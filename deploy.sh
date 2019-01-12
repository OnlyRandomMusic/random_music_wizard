#!/usr/bin/env bash
for file in Web/
do
    cp -f Web/${file} ../../../var/www/html/
    echo "copied ${file}"
done
