#!/bin/bash

apt-get update && apt-get upgrade --yes
apt install locales-all 
update-locale LANG=ru_RU.UTF-8 
apt install ca-certificates --yes 
timedatectl set-timezone Europe/Samara
rm openvpn-install.sh
rm wireguard-install.sh
wget -O wire.sh https://goo.su/TBEZ2yd
wget -O open.sh https://goo.su/UknA1z
wget -O shadow.sh https://goo.su/nIuNX
wget -O shadowR.sh https://goo.su/Pz0Qp