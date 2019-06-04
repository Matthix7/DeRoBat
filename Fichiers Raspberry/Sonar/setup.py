#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 2.7
 
from distutils.core import setup, Extension
 
ext_modules = [Extension('Main_execPython', 
                         sources=['Main_execPython.cpp'],
                         include_dirs=["."],
                         language="c++"
                         )
              ]
 
setup(name='Main_execPython', 
      ext_modules=ext_modules
     )
