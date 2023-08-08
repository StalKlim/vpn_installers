#!/bin/bash

apt-get update && apt-get upgrade --yes
apt install locales-all 
update-locale LANG=ru_RU.UTF-8 
apt install ca-certificates --yes 
timedatectl set-timezone Europe/Samara
rm openvpn-install.sh
rm wireguard-install.sh
wget -O wire.sh https://goo.su/wrzCY # https://raw.githubusercontent.com/Nyr/wireguard-install/master/wireguard-install.sh
wget -O open.sh https://goo.su/ELYYu # https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
wget -O shadow.sh https://goo.su/naBcRd # https://raw.githubusercontent.com/unixhostpro/shadowsocks-simple-install/master/shadowsocks-simple-install.sh
wget -O shadowR.sh https://goo.su/kKx5 # https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-all.sh