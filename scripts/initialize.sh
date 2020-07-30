#!/bin/bash

ci=${ci:-false}
token=${token:-}

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

    ./scripts/install-binaries.sh --ci ${ci}
    ./scripts/install-dependencies.sh --ci ${ci}
    ./scripts/start-services.sh --token ${token} --ci ${ci}

else
    echo "Initialization script is made to work with a Mac or Linux environment."
fi