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

echo ""
echo "Starting services"
echo ""

if [ "${machine}" == "Linux" ] && [ "${ci}" == "false"  ]
then

    echo ""
    echo "Starting VNC Server ..."
    echo ""

    # Ensure that VNC Server is started everytime the device is being rebooted
    sudo systemctl enable vncserver-x11-serviced.service #systemd
    update-rc.d vncserver-x11-serviced defaults #initd

    # Start VNC Server
    sudo systemctl start vncserver-x11-serviced.service #systemd
    /etc/init.d/vncserver-x11-serviced start #initd

fi

echo ""
echo "Generating SSL certificate"
echo ""

country="SE"
commonname="warehouse.langoon"
state="Stockholms Län"
locality="Stockholm"
organization="Langoon AB"
organizationalunit="IT"

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 13210 -nodes -subj "/C=$country/ST=$state/L=$locality/O=$organization/OU=$organizationalunit/CN=$commonname"

cert=$(<cert.pem)
key=$(<key.pem)

rm cert.pem
rm key.pem

# Close running instances of Node if any
ps aux | grep " node " | grep -v grep
nodepids=$(ps aux | grep " node " | grep -v grep | cut -c10-15)
for nodepid in ${nodepids[@]}
do
kill -9 $nodepid
done

echo ""
echo "Starting webserver ..."
echo ""

# Start webserver
DEVICE_TOKEN="${token}" SSL_KEY="${key}" SSL_CERT="${cert}" node webserver/start.js

if [ "${ci}" == "true"  ]; then
    sudo killall node
fi