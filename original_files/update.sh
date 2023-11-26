#!/bin/bash

apt-get update && apt-get upgrade --yes
apt install locales-all 
update-locale LANG=ru_RU.UTF-8 
apt install ca-certificates --yes 
timedatectl set-timezone Europe/Samara
rm openvpn-install.sh
rm wireguard-install.sh
mkdir vless

wget -O update.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/update.sh
wget -O wire.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/wire.sh
wget -O open.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/open.sh
wget -O shadow.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/shadow.sh
wget -O shadowR.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/shadowR.sh
wget -O vless.py https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/vless.py
wget -O vless/configgrpc.json https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/configgrpc.json
wget -O vless/configh2.json https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/configh2.json
wget -O vless/configxtls.json https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/configxtls.json