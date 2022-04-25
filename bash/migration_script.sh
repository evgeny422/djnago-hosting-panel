#!/bin/bash

cd $1
. venv/bin/activate
./manage.py makemigrations
./manage.py migrate
