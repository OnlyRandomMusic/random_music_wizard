#!/usr/bin/env bash
rm -rf venv

virtualenv venv
source venv/bin/activate
pip install requests
pip install deezloader
pip install simplejson
pip install flask
pip install python-vlc
