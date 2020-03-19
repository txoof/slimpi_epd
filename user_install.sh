#!/bin/bash
appName="slimpi"
projectURL="https://github.com/txoof/slimpi_epd/blob/master/README.md"
configPath="$HOME/.config/com.txoof.$appName"
configFile="$configPath/$appName.cfg"

if [[ ! -f $configFile ]]; then
  echo "creating configuration files"
  mkdir -p $configPath
  cp ./dist/slimpi/$appName.cfg $configPath
fi

echo "Please check $configFile for required configuration settings"
echo "$appName requires that 'player_name' and 'display' are set."
echo "See $projectURL"
