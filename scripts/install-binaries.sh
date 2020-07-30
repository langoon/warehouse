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

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac


echo ""
echo "Installing binaries"
echo ""

if [ "${machine}" == "Linux" ]; then

    # Don't upgrade if running on a CI environment as it will require a lot of time
    if [ "${ci}" == "false"  ]; then

        echo ""
        echo "Upgrading"
        echo ""

        sudo apt-get update
        sudo apt-get full-upgrade

    fi

    echo ""
    echo "Installing Flake8"
    echo ""

    sudo apt-get install flake8

    echo ""
    echo "Installing Zbar"
    echo ""

    sudo apt-get install libzbar0

    echo ""
    echo "Installing Tesseract"
    echo ""

    sudo apt install tesseract-ocr

    echo ""
    echo "Installing Node"
    echo ""

    curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
    sudo apt-get install -y nodejs

fi

if [ "${machine}" == "Mac" ]; then

    echo ""
    echo "Upgrading"
    echo ""

    sudo chown -R $(whoami) $(brew --prefix)/*

    brew upgrade

    echo ""
    echo "Installing Flake8"
    echo ""

    brew install flake8

    echo ""
    echo "Installing Zbar"
    echo ""

    brew install zbar

    echo ""
    echo "Installing Tesseract"
    echo ""

    brew install tesseract

    echo ""
    echo "Installing Node"
    echo ""

    brew install node

fi