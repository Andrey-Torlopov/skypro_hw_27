#!/bin/sh

poetry install
echo "requirements installed"
docker run --name hw_30_ps -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
echo ">>> docker started"
echo "finished"