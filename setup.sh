#!/bin/bash


source $VENV

cd $SOURCE

python3 setupdb.py

python3 setupconfig.py