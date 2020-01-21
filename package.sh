#/bin/bash
appName="slimpi"

version=`cat constants.py | sed -ne 's/version\W\{0,\}=\W\{0,\}\(.*\)["'"'"']/\1/p'`
echo version number is $version
filename=$appName\_$version.tgz
latestName=$appName\_latest.tgz

echo $filename

pipenv run pyinstaller --clean --noconfirm slimpi.spec

if [[ $? -eq 0 ]]; then

  tar cvzf $filename --transform 's,^,$appName/,' -T tarlist.txt
  cp $filename $latestName

else
  echo "error creating executable see output above for errors"
fi

# write case statement to only do this if --release

#  git add $filename
#  git commit -m "update build" $appName\_*.tgz

