#!/usr/bin/env python
# Copyright 2005 Michael Rice
# errr@errr-online.com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os,re,shutil,sys,tarfile
from os.path import expanduser

def set_style(style):
  
    '''Select style and create entry in init file to reflect, then restart flux for change to take place'''
    
    newStyleName = "session.styleFile:\t"+expanduser("~/.fluxbox/styles/"+style+"\n")
    oldStyleName = ""
    shutil.copyfile(expanduser("~/.fluxbox/init"),expanduser("~/.fluxbox/init.bckp"))
    cFile = open(expanduser("~/.fluxbox/init.bckp"),"r")
    text = cFile.readlines()
    cFile.close()
    input = open(expanduser("~/.fluxbox/init.bckp"),"r")
    styleLine = re.compile(r"session.styleFile")
    for x in text:
        if styleLine.search(x):
            oldStyleName = x 
    output = sys.stdout
    output =  open(expanduser("~/.fluxbox/init"),"w")
    for s in input.readlines():
        output.write(s.replace(oldStyleName,newStyleName))
    output.close()
    input.close()
    # attempt to not have to make a seperate fedora package for odd name
    # 'fluxbox-bin'
    os.system('kill -s HUP `xprop -root _BLACKBOX_PID | awk \'{print $3}\'`')
    return

def install_style(file):
    
    '''Install a valid tar.gz or tar.bz2 style foo.tar.gz/foo.tar.bz2 we check to see if it was  packaged as styleFoo/ or as ~/.fluxbox/styles/styleFoo people package both ways'''
    for i in file:
        #print i
        ins_dir = expanduser("~/.fluxbox/styles")
        if tarfile.is_tarfile(i) == True:
            # try first for bz2
            #print "its a tar file"
            try:
                tar = tarfile.open(i, "r:bz2")
                #maybe its tar.gz
            except tarfile.ReadError:
                try:
                    tar = tarfile.open(i, "r:gz")
                    #this isnt a bz2 or gz, so wtf is it?
                except tarfile.ReadError:
                    #now return 2 to say weird file type..
                    return 2
            #we need to find out how the style was packaged
            #if it is ~/.fluxbox/styles/styleName then we need a new
            #install dir. otherwise use default.
            check = tar.getnames()
            x = re.compile('^\.fluxbox/styles/.+')
            if x.match(check[0]) == None:
                for i in tar:
                    tar.extract(i,ins_dir)
                    #print i, ins_dir
            else:
                ins_dir = expanduser("~/")
                for i in tar:
                    tar.extract(i,ins_dir)
            
        else:
            # 2 == it wasnt even a tar file at all. This is a double check, we filter 
            #the file types in the file chooser to allow only tar.gz and tar.bz2
            return 2
    return
def remove_style(file):
  
    '''This can be used to remove a style'''
    
    #print "I will del "
    #for i in file:
    shutil.rmtree(expanduser('~/.fluxbox/styles/')+file)
    #shutil.rmtree('/tmp/errr/styles_fluxmod/'+file)
#install_style(raw_input("style file to install? "))

