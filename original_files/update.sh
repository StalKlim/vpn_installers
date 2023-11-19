#!/bin/bash

apt-get update && apt-get upgrade --yes
apt install locales-all 
update-locale LANG=ru_RU.UTF-8 
apt install ca-certificates --yes 
timedatectl set-timezone Europe/Samara
rm openvpn-install.sh
rm wireguard-install.sh
wget -O update.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/update.sh
wget -O wire.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/wire.sh
wget -O open.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/open.sh
wget -O shadow.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/shadow.sh
wget -O shadowR.sh https://raw.githubusercontent.com/StalKlim/vpn_installers/main/original_files/shadowR.sh
