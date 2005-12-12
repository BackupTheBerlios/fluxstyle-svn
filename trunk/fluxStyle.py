#!/usr/bin/env python
# Copyright 2005 Michael Rice
# errr@errr-online.com

""" fluxStyle

fluxStyle is a graphical style-manager for the fluxbox
window manager. Orignal version written by Michael Rice.
Many special thanks to Zan a.k.a. Lauri Peltonen for GUI 
Improvements & Bug Stomping. 

Released under GPL v2.

TODO 
- add XML support or installing styles to some other location to 
  be used as a default instead of the standard ~/.fluxbox/styles
- somehow support older styles and not put folders in the list 
  like folders that dont have anything to do with a style.
- fix any bugs that may still be there and unseen..
- add tray icon support (this is started will be done soon)
- convert install script to python. This will allow checking for
  libs so it doesnt have to be done in the main app.
  
"""
import sys
#sys.path.append("/usr/local/fluxStyle/mods")
sys.path.append("./mods")
import os,findStyles,parseConfig,errorMessage
from os.path import isfile,expanduser,isdir
try:
    import gtk

except:
    #gtk is missing but tkinter is part of standard 
    #python modules so give an error using it about what 
    #the user is missing.
    from Tkinter import *
    # set up the window itself
    top = Tk()
    message = Frame(top)
    message.master.title("fluxStlye Error")
    message.pack()
    error = """You do not have pyGTK installed\n\
please vist http://pygtk.org/ and install\nat least 2.4, \
and for best results get 2.6 or newer."""
    # add the widgets
    lMessage = Label(message, text = error)
    lMessage.pack()
    qButton = Button(message, text = "OK", command = message.quit)
    qButton.pack()
    # set the loop running
    top.mainloop()
    raise SystemExit

try:
    import gtk.glade

except:
    #we have gtk so give a gui message as to why this app will not work.
    #maybe we need to offer to open the browser to
    #http://ftp.gnome.org/pub/GNOME/sources/libglade/2.0/ 
    ver = sys.version[:5]
    message = """You need to install libglade2 
http://ftp.gnome.org/pub/GNOME/sources/libglade/2.0/ 
or set your PYTHONPATH correctly.
try: export PYTHONPATH=/usr/local/lib/python%s/site-packages/
or export PYTHONPATH=/usr/lib/python%s/site-packages/""" % (ver,ver)
    errorMessage.infoMessage(message)
    raise SystemExit

if gtk.pygtk_version < (2,3,90):
    #we do have gtk so lets tell them via gui that they need to update pygtk
    #maybe we should add a 'would you like to open a browser to pygtk.org ??
    message ="""PyGtk 2.3.90 or later required for this program 
it is reccomended that you get pygtk 2.6 or newer for best results."""
    errorMessage.infoMessage(message)
    raise SystemExit
  
class StyleChange:
    """Class wrapper for changing styles in fluxbox"""
    location = ""
    def main(self):
        gtk.main()
    
    def __init__(self):
        """The main fluxStyle window will show"""
        global location
        #gladefile="/usr/local/fluxStyle/images/main.glade"
        gladefile = "./images/main.glade"
        windowname = "window1"
        self.wTree = gtk.glade.XML (gladefile,windowname)
        self.treeview1 = self.wTree.get_widget("treeview1")
        self.view_menu = self.wTree.get_widget("view1_menu")
        self.__fill_view_menu__(self.view_menu)
        
        handler = {"on_apply_style_clicked":self.__apply_style_clicked__,
                   "on_quit_clicked":(gtk.main_quit),
                   "on_add_style_clicked":self.__add_style_clicked__,
                   "on_remove_style_clicked":self.__remove_style_clicked__,
                   "on_quit1_activate":(gtk.main_quit),
                   "on_about1_activate":self.__about1_activate__,
                   "on_window1_destroy":(gtk.main_quit),
                   "on_default1_activate":self.__fill_combolist__}
        
        self.wTree.signal_autoconnect (handler)

        #Preparing the treeview here
        self.liststore = gtk.ListStore(gtk.gdk.Pixbuf, str)
        self.treeview1.set_model(self.liststore)

        renderer = gtk.CellRendererText()
        imagerenderer = gtk.CellRendererPixbuf()
        imagerenderer.set_property('ypad', 10)
        imagerenderer.set_property('xpad', 5)
        column1 = gtk.TreeViewColumn("Preview", imagerenderer, pixbuf=0)
        column1.set_resizable(True)
        column2 = gtk.TreeViewColumn("Name", renderer, text=1)
        column2.set_resizable(True)
        self.treeview1.append_column(column1)
        self.treeview1.append_column(column2)

        #Fill it (Clear + fill)
        self.__fill_combolist__(self.treeview1,loc="default")
        return
    
    # Call backs begin here 
    # fill combo list    
    def __fill_combolist__(self,widget,loc="default"):
        """Fill the combo list with styles test to see if there is a ~/.fluxbox/styles
        if there isnt then make it and move on instead of die."""
        global location
        location = expanduser(loc)
        if location == "default":
            location = expanduser("~/.fluxbox/styles")
            try:
                dir = os.listdir(location)
                dir.sort()
                self.liststore.clear()
                for styles in dir:
                    if isdir(location+"/"+styles):
                        self.liststore.append((self.__get_preview__(styles), styles,))
            except(OSError):
                dir = expanduser("~/.fluxbox/styles")
                os.makedirs(dir,mode=0700)
                message = """You do not have a default\nstyle folder yet \
        I have\nmade it for you. The list will\nremain empty until you \ninstall a \
        style which you can\ndo by clicking the add button."""
                m = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, \
                    gtk.BUTTONS_NONE, message)
                m.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
                response = m.run()
                m.hide()
                if response == gtk.RESPONSE_CLOSE:
                    m.destroy()
        else:
            dir = os.listdir(location)
            dir.sort()
            self.liststore.clear()
            for styles in dir:
                if isdir(location+"/"+styles):
                    self.liststore.append((self.__get_preview__(styles), styles,))
    # get the preview image for view
    def __get_preview__(self, stylename):
        """Get the preview image from  ~/.fluxbox/styles/styleName/preview.jpg"""
        global location
        location = expanduser(location)
        if os.path.isdir(location + "/" + stylename):
            if isfile(location+"/"+stylename+"/preview.jpg"):
                image = gtk.Image()
                image.set_from_file(location+"/" +stylename+"/preview.jpg")
                return image.get_pixbuf()
            else:
                image = gtk.Image()
                #image.set_from_file( "/usr/local/fluxStyle/images/none.jpg")
                image.set_from_file( "./images/none.jpg")
                return image.get_pixbuf()
    def __fill_view_menu__(self, widget):
        #TODO check to see if ops == False if so then the config hasnt been edited yet
        #so all we have is our default style location.
        if parseConfig.check4_config() == 2:
            message = """This looks like the first time you have started fluxStlye
a default config has been created for you. You should edit this config to control the
location of styles shown in the preview window. The config file is located in ~/.fluxStyle.rc"""
            errorMessage.infoMessage(message)
        
        elif parseConfig.check4_config() == 3:
            message = """You do not have the config file "~/.fluxStyle.rc" and you do not have write access
to the "~/" aka $HOME directory. If you find this is not accurate information please report a bug to errr@errr-online.com"""
            errorMessage.infoMessage(message)
        elif parseConfig.check4_config() == True:
            ops = parseConfig.parse_file(expanduser("~/.fluxStyle.rc"))
            if ops != False:
                count = 1
                view = self.view_menu
                for k,v in ops.iteritems():
                    if k == "STYLES_DIRS":
                        for x in v:
                            name = "_"+str(count)+" Extra Styles"
                            menuitem = gtk.MenuItem(name + str(count))
                            menuitem.connect("activate", self.__fill_combolist__,x)
                            view.add(menuitem)
                            count += 1
                    view.show_all()            
    # Set style 
    def __apply_style_clicked__(self,widget):
        """Used to apply new styles"""
        global location
        style = self.__get_selected_style__()
        if style:
            findStyles.set_style(style,location)

    # Add style
    def __add_style_clicked__(self,widget):
        """Install a new style, multiple styles can be installed at once."""
        
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
        filter.add_pattern("*.tgz")
        dialog.add_filter(filter)
        dialog.set_select_multiple(True)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            findStyles.install_style(dialog.get_filenames())
            self.__fill_combolist__(self)
            dialog.destroy()
        if response == gtk.RESPONSE_CANCEL:
            dialog.destroy()
    
    # remove style
    def __remove_style_clicked__(self,widget):
        """Remove selected style, currently only 1 style at a time is supported"""
        global location
        style = self.__get_selected_style__()
        if style == False:
            m = """You must select a style to remove first"""
            errorMessage.infoMessage(m)            
        else:
            message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, \
                gtk.BUTTONS_NONE, "Are you sure you want to delete %s?"%(style))
            message.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
            message.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE)
            response = message.run()
            message.hide()
            if response == gtk.RESPONSE_OK:
                if findStyles.remove_style(style,location) != False:
                    message.destroy()
                    self.__fill_combolist__(self,location)
                else:
                    say = """You do not have access to remove this style please contact your system admin for help removing this style."""
                    message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, say)
                    message.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
                    response = message.run()
                    message.hide()
                if response == gtk.RESPONSE_CLOSE:
                    message.destroy()
            if response == gtk.RESPONSE_CLOSE:
                message.destroy()
    def __get_selected_style__(self):
        """Getting the selected style"""
        selection = self.treeview1.get_selection()
        (model, iter) = selection.get_selected()
        if model and iter:
            return model.get_value(iter, 1)
        else:
            return False
    
    def __about1_activate__(self,widget):
        """Activate the help button with the about dialog, use generic if pygtk < 2.5.9"""
        #gladefile="/usr/local/fluxStyle/images/main.glade"
        gladefile="./images/main.glade"
        if gtk.pygtk_version < (2,5,90):
            message = """fluxStyle version 1.0 Updae your pygtk version for more features. Version
2.6.0 or newer is reccomended"""
            errorMessage.infoMessage(message)
        else:
            windowname2="aboutdialog1"
            self.wTree2=gtk.glade.XML (gladefile,windowname2)
if __name__ == "__main__":
    style = StyleChange()
    style.main()
