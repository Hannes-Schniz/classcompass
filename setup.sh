#!/bin/bash


source $VENV

cd $SOURCE

python3 setup/setupdb.py

python3 setup/setupconfig.py

# TODO: move setup files in setup folder    