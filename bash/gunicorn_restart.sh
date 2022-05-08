#!/bin/bash

cd $1

sudo systemctl restart gunicorn
sudo systemctl restart nginx