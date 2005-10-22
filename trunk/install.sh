#!/bin/bash
# lame install script, can you make it better?
# if so send it to me errr@errr-online.com
# thanks

if [ $1 !="install" ]; then
  echo "

Currently this is setup to be run from local dir, there is
no need to install this. Simply: chmod +x fluxStyle  and then
run this from the directory you downloaded it with the following
command: ./fluxStyle 

If you want to install it then run as root using 
"
  exit
fi

INSDIR="/usr/local/fluxStyle"
BINDIR="/usr/local/bin"
WHO="`whoami`"

if [ ! -w $BINDIR ]; then
  echo "You dont have access to write to $BINDIR"
fi

if [ $WHO != "root" ]; then
  echo "You must be root to run this"
  exit
fi

if [ ! -d $INSDIR ]; then 
  mkdir -p $INSDIR
fi

if [ ! -d $BINDIR ]; then
  mkdir -p $BINDIR
fi

cp -R `pwd`/images $INSDIR
cp -R `pwd`/mods $INSDIR
install -m755 fluxStyle $BINDIR
echo "If there were no errors fluxStyle is installed and ready for use."
