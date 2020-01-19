#!/bin/bash
pipenvExec=`which pipenv`

if [[ -x ${pipenvExec} ]]; then
  echo "sync pipenv"
  # may need to manually install the following packages due to ????
  #pipenv install Pillow
  #pipenv install RPi.GPIO
  #pipenv sync
else
  echo "building requires pipenv use:
$ sudo pip3 install pipenv"
  exit
fi

echo "building slimpi media player"
#pipenv run pyinstaller --noconfirm slimpi.spec

