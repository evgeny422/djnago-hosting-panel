#!/bin/bash

if [[ -e $1 ]]
then
    cd $1
    . venv/bin/activate
    ./manage.py collectstatic
fi