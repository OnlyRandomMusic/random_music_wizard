#!/usr/bin/env bash

git pull
cp -rf web /var/www/
sudo systemctl reload apache2
