#!/bin/bash

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

if [ "${machine}" == "Linux" ] || [ "${machine}" == "Mac" ]
then

    sudu scrips/install-binaries.sh
    sudu scrips/install-dependencies.sh
    sudu scrips/start-services.sh

else
    echo "Initialization script is made to work with a Mac or Linux environment."
fi