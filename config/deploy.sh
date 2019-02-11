#!/usr/bin/env bash
cp -rf web ../../../var/www/
sudo systemctl reload apache2
