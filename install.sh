#!/bin/bash
appName="slimpi"
installPath="/usr/bin/slimpi/"
sysdService="./install/$appName-daemon.service"

if [ "$EUID" -ne 0 ]
  then 

    echo "
This installer must be run as root.

Try: 
    $ sudo `basename "$0"`

The installer will setup $appName to run at system boot by doing the following:
    * Install $appName files in $installPath
    * Create configuration files in /etc/
    * Setup systemd scripts
    * Create user and group 'slimpi' to run the system daemon
    * Add user 'slimpi' to the GPIO and SPI access groups

To uninstall use:
    # `basename "$0"` --uninstall 
    "
  exit
fi
# add the user
useradd --system $appname

# copy program files to $installPath
cp -r ./dist/slimp $installPath

usermod -a -G spi,gpio $appName

chown --recursive $installPath $appName.$appName

cp -s $sysdService /etc/systemd/user/ `basename $sysdService`
