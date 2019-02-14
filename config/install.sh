#!/usr/bin/env bash
sudo apt update
sudo apt upgrade

sudo apt-get install apache2
sudo apt-get install vlc
#sudo apt-get install virtualenv
sudo apt-get install sqlite3

bash config/install_short.sh
bash config/web_config

# things to do manually:
# change pi user (cf. https://gordonlesti.com/change-default-users-on-raspberry-pi/)
##adduser rengati (use a simple password and change it at the end of the procedure)
##adduser rengati sudo
## (set boot mode to CLI without autologin in raspi-config)
## (logout and then login with new username)
##sudo deluser pi
##sudo passwd root
## (maybe change autologin-user)
## (set boot mode to Desktop with autologin in raspi-config)

# enable ssh (and VNC)
# static IP configuration (/etc/dhcpcd.conf)
# ethernet local IP configuration (/boot/cmdline.txt add ip=169.254.51.51 and change 51 by the number you want)
# (if needed reconfigure network with raspi-config)
# git clone and then run this script

# line to add in rc.local to start on boot:
# su rengati -c "python3 home/rengati/random_music_wizard/main.py &"
