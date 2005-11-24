'''Written by Michael Rice
Copyright Nov 14, 2005
Released under the terms of the GNU GPL v2
Email: Michael Rice errr@errr-online.com
Website: http://errr-online.com/
'''
import os,re

def parse_file(file):
    """read config file place results into a 
    dict file location provided by caller. 
    keys = options (USEICONS, ICONPATHS, etc)
    values = values from options
    config file should be in the form of:
    OPTION:values:moreValuse:evenMore
    do not end with ":"  Comments are "#" as 
    the first char.
    #OPTION:commet
    OPTION:notComment #this is not valid comment
    """
    opts = {}
    if os.path.isfile(file):
        match = re.compile(r"^[^#^\n]")
        f = open(file)
        info = f.readlines()
        f.close()
        keys = []
        for lines in info:
            if match.findall(lines):
                keys.append( lines.strip().split(":") )
    for i in range(len(keys)):
        opts[keys[i][0]] = keys[i][1:]
    return opts
#if __name__ == "__main__":
#    parse_file("/home/errr/fluxmenu/testConfig")
