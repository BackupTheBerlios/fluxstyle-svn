#!/bin/bash
# lame install script, can you make it better?
# if so send it to me errr@errr-online.com
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
