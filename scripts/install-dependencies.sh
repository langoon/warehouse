#!/bin/bash

ci=${ci:-false}

while [ $# -gt 0 ]; do

   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
        # echo $1 $2 // Optional to see the parameter:value result
   fi

  shift
done

echo ""
echo "Installing dependencies"
echo ""

if [ "${ci}" == "true"  ]
then
    pip install -r requirements.txt 
else
    pip3 install -r requirements.txt 
fi