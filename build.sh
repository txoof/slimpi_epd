#!/bin/bash
pipenvExec=`which pipenv`

# check if libopen and libtiff are installed
# apt -qq list libopenjp2-7-dev
# apt -qq list `libbtiff5-dev

if [[ -x ${pipenvExec} ]]; then
  echo "pipenv --three; pipenv sync"
  #pipenv --three
  #pipenv sync
else
  echo "building requires pipenv use:
$ sudo pip3 install pipenv"
  exit
fi

echo "building slimpi media player"
#pipenv run pyinstaller --noconfirm slimpi.spec

