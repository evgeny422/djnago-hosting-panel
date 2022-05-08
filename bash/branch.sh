#!/bin/bash

if [[ -e $1 ]]
then
    cd $1
    git checkout $3
fi

