#!/bin/bash
appName="slimpi"
installPath="/usr/bin/slimpi/"
sysConfig="./$appName.cfg"
serviceName=$appName-daemon
sysdService="./install/$serviceName.service"

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

install () {
  # add the user
  useradd --system $appName

  # add the user to the appropriate groups
  usermod -a -G spi,gpio $appName

  # copy program files to $installPath
  cp -r ./dist/$appName $installPath

  # copy the system configuration into /etc/
  cp $sysConfig /etc/

  # install the systemd unit file
  cp $sysdService /etc/systemd/system/

  # start the service
  systemctl enable $serviceName

  echo "Please configure $appName by editing /etc/$appName.cfg
  HINT: $ sudo nano /etc/$appName.cfg

The following MUST be updated for *your* system:
  * player_name = <player to be monitored> 
      - available players can be found by running: 
        $installPath/$appName -s
  * display = <epd type>

Once configured, start $appName with:
  $ sudo systemctl start $serviceName

$appName will now start when this system is booted.
"
}


uninstall () {
  echo "uninstalling $appName"
  if [ "$1" == "-p" ] || [ "$1" == "--purge" ]
  then
    echo "purging system configuration files"
    rm /etc/$appName.cfg
  fi

  systemctl stop $serviceName
  systemctl disable $serviceName
  rm /etc/systemd/system/$serviceName.service

  userdel $appName

  rm -r $installPath

}

if [ $# -eq 0 ]; then
  install
else
  case $1 in
    -u|--uninstall)
      uninstall $2;;
    -h|--help|*)
      echo "Unknown argument: $1

use:
  * install $appName: $ $0
  * uninstall $appName: $ $0 -u|--uninstall 
  * uninstall $appName and purge configuration files: 
    $ $0 -u|--uninstall [-p|--Purge]"
esac
fi
