#!/bin/sh


py -m venv env
echo ">>> nv created"
source ./env/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
echo ">>> requirements installed"
docker run --name hw_30_ps -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
echo ">>> docker started"
echo "finished"