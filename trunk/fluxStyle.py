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


try:
    import pygtk
    #tell pyGTK, if possible, that we want GTKv2
    pygtk.require("2.0")
except:
    #Some distributions come with GTK2, but not pyGTK
    pass
try:
    import gtk
    import gtk.glade
except:
    import sys
    print "You need to install pyGTK or GTKv2, or libglade2",
    print "or set your PYTHONPATH correctly."
    print "try: export PYTHONPATH=",
    print "/usr/local/lib/python2.2/site-packages/"
    sys.exit(1)
if gtk.pygtk_version < (2,3,90):
    print "PyGtk 2.3.90 or later required for this program\
        it is reccomended that you get pygtk 2.6 or newer for best results."
    raise SystemExit

import os,findStyles,re
from os.path import isfile,expanduser
#now we have both gtk and gtk.glade imported
#Also, we know we are running GTK v2
class StyleChange:
    def __init__(self):

        """The main fluxStyle window will show"""
        
        gladefile="/usr/local/fluxStyle/images/main.glade"
        windowname="window1"
        self.wTree=gtk.glade.XML (gladefile,windowname)
        self.combobox1=self.wTree.get_widget("comboboxentry1")
        self.image1=self.wTree.get_widget("image1")
        self.fill_combolist(self.combobox1)
        handler = {"on_button1_clicked":self.button1_clicked,
                   "on_button2_clicked":(gtk.main_quit),
                   "on_button3_clicked":self.button3_clicked,
                   "on_button4_clicked":self.button4_clicked,
                   "on_comboboxentry1_changed":self.combobox1_changed,
                   "on_quit1_activate":(gtk.main_quit),
                   "on_about1_activate":self.about1_activate,
                   "on_window1_destroy":(gtk.main_quit)}
        
        self.wTree.signal_autoconnect (handler)
        return
    
    # Call backs begin here 
    # start with buttons
    # Set style 
    def button1_clicked(self,widget):
        model = self.combobox1.get_model()
        index = self.combobox1.get_active()
        if index > -1:
            style = model[index][0]
            findStyles.set_style(style)
            
    # Add style
    def button3_clicked(self,widget):
        dialog = gtk.FileChooserDialog("Choose file to install",
                                        None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("Fluxbox Styles")
        filter.add_mime_type("tar/gz")
        filter.add_mime_type("tar/bz2")
        filter.add_pattern("*.tar.gz")
        filter.add_pattern("*.tar.bz2")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            findStyles.install_style(dialog.get_filename())
            self.fill_combolist(self)
            dialog.destroy()
        if response == gtk.RESPONSE_CANCEL:
            dialog.destroy()
    
    # remove style
    def button4_clicked(self,widget):
        model = self.combobox1.get_model()
        index = self.combobox1.get_active()
        #print "button 4 clicked (remove style) "+model[index][0]
        message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, \
            gtk.BUTTONS_NONE, "Are you sure you want to delete "+model[index][0]\
            +"?")
        message.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        message.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE)
        response = message.run()
        message.hide()
        if response == gtk.RESPONSE_OK:
            findStyles.remove_style(model[index][0])
            message.destroy()
            self.fill_combolist(self)
        if response == gtk.RESPONSE_CLOSE:
            message.destroy()
    
    def fill_combolist(self,widget):
        dir = os.listdir(expanduser("~/.fluxbox/styles"))
        dir.sort()
        self.combobox1=self.wTree.get_widget("comboboxentry1")
        liststore = gtk.ListStore(str)
        for styles in dir:
            liststore.append([styles])
        self.combobox1.set_model(liststore)
    
    def combobox1_changed(self,widget):
        model = self.combobox1.get_model()
        index = self.combobox1.get_active()
        #pic = re.compile(r'\.(jpg|jpeg|png)$', re.IGNORECASE)
        if index > -1:
            self.image1=self.wTree.get_widget("image1")
            if isfile(expanduser("~/.fluxbox/styles/"+model[index][0]+"/preview.jpg")):
                self.image1.set_from_file(expanduser("~/.fluxbox/styles/"\
                    +model[index][0]+"/preview.jpg"))
            else:
                self.image1.set_from_file("/usr/local/fluxStyle/images/none.jpg")
        return
    
    def about1_activate(self,widget):
        gladefile="/usr/local/fluxStyle/images/main.glade"
        if gtk.pygtk_version < (2,5,90):
            message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, \
                gtk.BUTTONS_NONE, \
                "fluxStyle version 1.0\nUpdae your pygtk version\nfor more features."+\
                " Version\n2.6.0 or newer is reccomended")
            message.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
            response = message.run()
            message.hide()
            if response == gtk.RESPONSE_OK:
                message.destroy()            
        else:
            windowname2="aboutdialog1"
            self.wTree2=gtk.glade.XML (gladefile,windowname2)

app=StyleChange()
gtk.main()   
