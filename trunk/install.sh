#!/bin/bash
# lame install script, can you make it better?
# if so send it to me errr@errr-online.com
# thanks
i=$1
close='\033[0m'
yellow="\033[0;33;40m"
green="\033[0;32;40m"
red="\033[0;31;40m"

if [ ! $i ]; then
  printf $green
  echo "
Currently this is setup to be run from local dir, there is
no need to install this. Simply: chmod +x fluxStyle  and then
run this from the directory you downloaded it with the following
command: ./fluxStyle

If you want to install it then run as root using ./install install
"
  printf $close
  printf $yellow
  echo "
******************************************************************
*********You should make these changes BEFORE you install*********
******************************************************************"
  printf $close
  printf $green
  echo "
You will need to edit some of the fluxStyle source. Comment out line 
94 and uncomment 93, Comment out 113 and uncomment 112, comment out 
line 245 and uncomment 244 uncomment 259 and comment 260."
  printf $close
  printf $red
  echo "
Please note as development changes the lines to edit will change
and I will not keep this info updated, so only install offical 
releases unless you know what you are doing!!
"
  printf $close
  exit
fi


if [ $i != "install" ]; then
    echo "proper syntax is: ./install install "
  exit
else 
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
fi
