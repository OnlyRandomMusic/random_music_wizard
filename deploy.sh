#!/usr/bin/env bash
for file in Web/*
do
    cp -rf ${file} ../../../var/www/
    echo "copied ${file}"
done
