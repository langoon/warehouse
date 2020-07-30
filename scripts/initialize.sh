#!/bin/bash

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

if [ "${machine}" == "Mac" ]
then

    # Check for Homebrew, install if we don't have it
    if test ! $(which brew); then
        echo "Installing homebrew"
        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    fi

fi

if [ "${machine}" == "Linux" ] || [ "${machine}" == "Mac" ]
then

    ./scripts/install-binaries.sh
    ./scripts/install-dependencies.sh
    ./scripts/start-services.sh ${1}

else
    echo "Initialization script is made to work with a Mac or Linux environment."
fi