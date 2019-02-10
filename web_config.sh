#!/usr/bin/env bash
sudo apt-get install libapache2-mod-wsgi python-dev
sudo a2enmod wsgi

sudo bash deploy.sh

sudo mkdir ../../../var/www/flask_server
sudo mkdir ../../../var/www/flask_server/logs
sudo cp -rf config/flask_server.conf ../../../etc/apache2/sites-available/flask_server.conf

sudo a2ensite flask_server.conf

sudo systemctl reload apache2
