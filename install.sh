#!/usr/bin/env bash
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install apache2
sudo apt-get install vlc
sudo apt-get install virtualenv
sudo apt-get install sqlite3

bash deploy.sh
bash install_short.sh
