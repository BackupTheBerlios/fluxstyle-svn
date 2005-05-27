import os,re,shutil,sys,tarfile
from os.path import expanduser

def set_style(style):
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
    os.system('killall -s HUP fluxbox')
    return

def install_style(file):
    ins_dir = expanduser("/tmp/errr")
    if tarfile.is_tarfile(file) == True:
        # try first for bz2
        #print "its a tar file"
        try:
          tar = tarfile.open(file, "r:bz2")
        #maybe its tar.gz
        except tarfile.ReadError:
            try:
              tar = tarfile.open(file, "r:gz")
            #this isnt a bz2 or gz, so wtf is it?
            except tarfile.ReadError:
                #now return 5 to say weird file type..
                return 5
         
        for i in tar:
            tar.extract(i,ins_dir)
            #print i, ins_dir
    else:
        # 2 == it wasnt even a tar file at all.
        return 2
    return
  
#install_style(raw_input("style file to install?"))

