#!/bin/bash

apt-get update && apt-get upgrade --yes
apt install locales-all 
update-locale LANG=ru_RU.UTF-8 
apt install ca-certificates --yes 
timedatectl set-timezone Europe/Samara
wget -O wire.sh https://goo.su/wrzCY # https://raw.githubusercontent.com/Nyr/wireguard-install/master/wireguard-install.sh
wget -O open.sh https://goo.su/ELYYu # https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
wget -O shadow.sh https://goo.su/kKx5 # https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-all.sh