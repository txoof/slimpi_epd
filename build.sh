#!/bin/bash

echo "attempting to configure build environment and build SlimPi"


reqPackages=("libtiff5-dev" "libopenjp*-dev")
halt=0

for i in "${reqPackages[@]}"
do
  echo checking package $i
  if [ $(dpkg-query -W -f='${Status}' $i 2>/dev/null | grep -c "ok installed") -eq 0 ];
  then
    echo package: $i not installed. Install with:
    echo $ sudo apt-get install $i
    echo ""
    halt=$((halt+1))
  else
    echo $i...ok
    echo ""
  fi
done

if [[ $halt -gt 0 ]]; then
  echo "$halt critical packages missing. See messages above."
  echo "stopping here"
  exit
fi

pipenvExec=`which pipenv`

echo "checking pipenv virtual environment"

if [[ -x ${pipenvExec} ]]; then
  # check if there's a virutal environment
  pipenv --venv 2>/dev/null
  if [[ $? -ne 0 ]]; then
    echo "building pipenv virtual environment"
    pipenv --three
    pipenv lock
    pipenv sync
  else
    echo "sycning packages"
    echo pipenv sync
    pipenv lock
    pipenv sync
  fi
else
  echo "building requires pipenv use:
$ sudo pip3 install pipenv"
  exit
fi

echo "building slimpi media player"
pipenv run pyinstaller --clean --noconfirm slimpi.spec

