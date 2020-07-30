#!/bin/bash

echo ""
echo "Starting services"
echo ""

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

if [ "${machine}" == "Linux" ]; then

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
node webserver/start.js