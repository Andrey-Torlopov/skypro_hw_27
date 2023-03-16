#!/bin/sh


py -m venv env
echo ">>> nv created"
source ./env/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
echo ">>> requirements installed"
echo "ok"