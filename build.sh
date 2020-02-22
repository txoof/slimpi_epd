#!/bin/bash

echo "attempting to configure build environment and build SlimPi"


reqPackages=("libtiff5-dev" "libopenjp*-dev")

for i in "${reqPackages[@]}"
do
  echo checking package $i
  if [ $(dpkg-query -W -f='${Status}' $i 2>/dev/null | grep -c "ok installed") -eq 0 ];
  then
    echo package: $i not installed. Install with:
    echo $ sudo apt-get install $i
    echo ""
  else
    echo $i...ok
    echo ""
  fi
done


pipenvExec=`which pipenv`

echo "checking pipenv virtual environment"

if [[ -x ${pipenvExec} ]]; then
  # check if there's a virutal environment
  pipenv --venv 2>/dev/null
  if [[ $? -ne 0 ]]; then
    echo "building pipenv virtual environment"
    pipenv --three
    pipenv sync
  else
    echo "sycning packages"
    echo pipenv sync
    pipenv sync
  fi
else
  echo "building requires pipenv use:
$ sudo pip3 install pipenv"
  exit
fi

echo "building slimpi media player"
pipenv run pyinstaller --clean --noconfirm slimpi.spec

