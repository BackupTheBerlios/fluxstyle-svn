#!/bin/bash
INSDIR="/usr/local/fluxStyle"
#IMGDIR="/usr/local/fluxStyle/images"
#MODDIR="/usr/local/fluxStyle/mods"
BINDIR="/usr/local/bin"

if [ ! -d $INSDIR ]; then 
  mkdir -p $INSDIR
fi
if [ ! -d $BINDIR ]; then
  mkdir -p $BINDIR
fi

cp -R `pwd`/images $INSDIR
cp -R `pwd`/mods $INSDIR
install -m755 fluxStyle $BINDIR
