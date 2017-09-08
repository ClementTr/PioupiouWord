#!/bin/bash

#Colors attribution
red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

echo "${red}Welcome on my Vagrant-VM${reset}"

# Install everything we will need in our VM (pip/virtualenv/etc.)
apt-get update
apt-get -y install -y python-pip
apt-get -y install python3-pip
apt-get -y install -y python-dev
sudo apt-get -y install python-qt4 pyqt4-dev-tools

