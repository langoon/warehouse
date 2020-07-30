#!/bin/bash

echo ""
echo "Installing dependencies"
echo ""

if [ -z "${!CI}" ]
then
    pip3 install -r requirements.txt 
else
    pip install -r requirements.txt 
fi