#!/bin/bash

if [[ $# -lt 2 ]]
then
    echo "Not all params was given"
    exit
fi

if [[ -e $1 ]]
then
    cd $1
    git pull $2
fi
