import json
import os
import re
import subprocess

xtls_path = "confvl/configxtls.json"
h2_path = "confvl/configh2.json"
grpc_path = "confvl/configgrpc.json"
config_path = "/usr/local/etc/xray/config.json"


def install_xray():
    os.system("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install -u root --version 1.8.3")


def enablebbr():
    try:
        if "net.core.default_qdisc=fq" in open("/etc/sysctl.conf").read():
            print("BBR is already enabled.")
            return
        else:
            print("Enabling BBR...")
            os.system("echo \"net.core.default_qdisc=fq\" >> /etc/sysctl.conf")
            os.system("echo \"net.ipv4.tcp_congestion_control=bbr\" >> /etc/sysctl.conf")
            os.system("sudo sysctl -p")
    except:
        print("failed to activate BBR.")


def generate_variables():
    global private_key
    global public_key
    global uuid
    global shortid
    global serverip

    # генерация публичного и приватного ключа
    x25519 = subprocess.check_output("xray x25519", shell=True)
    privkey_str = x25519.decode("utf-8")

    private_key = privkey_str[13:57]
    public_key = privkey_str[69:112]

    # генерация uuid
    uuid_byte = subprocess.check_output("xray uuid", shell=True)
    uuid = uuid_byte.decode("utf-8").rstrip()

    # генерация shortid
    shortid_btye = subprocess.check_output("openssl rand -hex 8", shell=True)
    shortid = shortid_btye.decode("utf-8").rstrip()

    # получение public_ip
    serverip_resp = os.popen('curl checkip.amazonaws.com').read()
    serverip = serverip_resp.replace("\n", "")


def createconfig(config_type, sni_dest="www.samsung.com", port=443):
    with open(config_type, "r") as f:
        data = json.load(f)

        # uuid
        data["inbounds"][0]["settings"]["clients"][0]["id"] = uuid.rstrip()

        # private_key
        data["inbounds"][0]["streamSettings"]["realitySettings"]["privateKey"] = private_key.rstrip()

        # shortids
        data["inbounds"][0]["streamSettings"]["realitySettings"]["shortIds"][0] = shortid.rstrip()

        # sni
        data["inbounds"][0]["streamSettings"]["realitySettings"]["serverNames"][0] = sni_dest

        data["inbounds"][0]["streamSettings"]["realitySettings"]["dest"] = f"{sni_dest}:443"

        # port
        data["inbounds"][0]["port"] = port

    with open("/usr/local/etc/xray/config.json", "w") as f:
        json.dump(data, f, indent=4)


def createfile(link, locname, tectype):
    with open(f"{locname}-VLESS.txt", "w") as file:
        file.write(f"V2RAY VLESS LINK (копируй начиная с vless:// и заканчивая TG_https://t.me/dedvpn): \n\n{link}\n\n"
                   "Инструкции по использованию найдешь по ссылке https://telegra.ph/Nastrojka-VPN-na-razlichnyh-ustrojstvah-07-24\n"
                   "Тебе понадобится инструкция \"Настройка V2RAY (VLESS) на *твой тип устройства*\"\n\n"
                   f"Техническая информация! (Нужно для поддержки) Тип подключения: {tectype}")


def createlink(type, sni, port, filename):
    locname = filename

    if type == "h2":

        os.system("clear")
        print(f">>> Конфигурация успешно создана :) <<<\n>>> НИЖЕ ССЫЛКА + СОЗДАН ФАЙЛ {filename}-VLESS.txt <<<\n")
        link = f"""vless://{uuid}@{serverip}:{port}?path=%2F&security=reality&encryption=none&pbk={public_key}&fp=chrome&type=http&sni={sni}&sid={shortid}#TG_https://t.me/dedvpn""".replace(
                " ", "")
        print(link)
        tectype = "Vless-h2-uTLS-Reality"
        createfile(link, locname, tectype)
        os.system("systemctl restart xray")
        os.system("systemctl enable xray")

    elif type == "xtls":

        os.system("clear")
        print(f"Конфигурация успешно создана :).\nВОТ ССЫЛКА + СОЗДАН ФАЙЛ {filename}-VLESS.txt : \n")
        link = f"""vless://{uuid}@{serverip}:{port}?security=reality&encryption=none&pbk={public_key}&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni={sni}&sid={shortid}#TG_https://t.me/dedvpn""".replace(
                " ", "")
        print(link)
        tectype = "Vless-XTLS-uTLS-Reality"
        createfile(link, locname, tectype)
        os.system("systemctl restart xray")
        os.system("systemctl enable xray")

    elif type == "grpc":

        os.system("clear")
        print(f"Конфигурация успешно создана :).\nВОТ ССЫЛКА + СОЗДАН ФАЙЛ {filename}-VLESS.txt : \n")
        link = f"""vless://{uuid}@{serverip}:{port}?mode=multi&security=reality&encryption=none&pbk={public_key}&fp=chrome&type=grpc&serviceName=grpc&sni={sni}&sid={shortid}#TG_https://t.me/dedvpn""".replace(
                " ", "")
        print(link)
        tectype = "Vless-grpc-uTLS-Reality"
        createfile(link, locname, tectype)
        os.system("systemctl restart xray")
        os.system("systemctl enable xray")


def xtls_reality(sni, port, filename):
    install_xray()
    enablebbr()
    generate_variables()
    createconfig(xtls_path, sni, port)
    createlink("xtls", sni, port, filename)


def h2_reality(sni, port, filename):
    install_xray()
    enablebbr()
    generate_variables()
    createconfig(h2_path, sni, port)
    createlink("h2", sni, port, filename)


def grpc_reality(sni, port, filename):
    install_xray()
    enablebbr()
    generate_variables()
    createconfig(grpc_path, sni, port)
    createlink("grpc", sni, port, filename)


def delete_reality():
    os.system("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ remove")


def exit():
    pass


def manual_mode():
    # manually take sni and port from the user
    os.system("clear")

    mode = input("Выбери протокол : \n1. VLESS-XTLS-uTLS-Reality (Рекомендуется) \n2. VLESS-grpc-uTLS-Reality \n3. Vless-h2-uTLS-Reality \nВведите значение:  ")

    if mode == "":
        print("Мод : XTLS")
        mode = "1"

    sni = input("Введите SNI (www.samsung.com по умолчанию): ")

    if sni == "":
        sni = "www.samsung.com"
        print(f">>> Вставлено значение по умолчанию {sni}")

    try:
        filename = input("Укажите ID сервера (FIN51/FR74): ")
    except (TypeError, ValueError):
        pass

    try:
        port = int(input("Введите порт (по умолчанию : 443): "))
    except (TypeError, ValueError):
        pass

    if mode == "1":
        xtls_reality(sni, port, filename)
    if mode == "2":
        grpc_reality(sni, port, filename)
    if mode == "3":
        h2_reality(sni, port, filename)


def menu():
    os.system("clear")
    mode = int(input(
        "Выберите опцию : \n1. Установка VLESS \n2. Удаление \n3. Выход \nВведите значение: "))
    if mode == 1:
        manual_mode()
    elif mode == 2:
        delete_reality()
    elif mode == 3:
        exit()


try:
    menu()
except ValueError:
    print("неправильный ввод")
    exit()
except KeyboardInterrupt:
    print("Надеемся увидеть тебя снова!")
    exit()
