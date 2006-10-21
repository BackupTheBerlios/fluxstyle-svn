#!/usr/bin/env python
"""Fluxstyle is a graphical style manager built in python using pygtk and glade.
Fluxstyle is for the fluxbox window manager. Orignal version written by Michael Rice.
Many special thanks to Zan a.k.a. Lauri Peltonen for GUI Improvements & Bug Stomping.

Released under GPL"""
from distutils.core import setup

doclines = __doc__.split("\n")

setup(name='fluxstyle',
      version='1.0.1',
      description=doclines[0],
      author='Michael Rice',
      author_email='errr@errr-online.com',
      url='http://fluxstyle.berlios.de/',
      packages=['fluxstyle'],
      data_files=[('/usr/share/fluxstyle-1.0/images',
        ['images/fluxmetal.png','images/mini-fluxbox6.png','images/none.jpg']),
        ('/usr/share/fluxstyle-1.0/glade',['images/main.glade']),
        ('/usr/bin',['bin/fluxStyle']),
        ('/usr/share/fluxstyle-1.0/docs',['docs/README','docs/LICENSE','docs/Changelog'])]
      )
