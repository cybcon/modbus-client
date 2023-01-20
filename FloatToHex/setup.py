#!/usr/bin/python3
# -*- coding: utf-8 -*-
# setup.py sdist      to create a package which can be uploaded to PyPi registry (but need more information)
# setup.py install    to install the package - needs C compiler (vcvarsall.bat on windows)


from distutils.core import setup, Extension

FloatToHexModule = Extension('FloatToHex',
                         sources = ['floattohexmodule.c'])

setup (name = 'FloatToHex',
       version = '1.0',
       url = 'https://gregstoll.com/~gregstoll/floattohex/',
       author = 'Gregory Stoll',
       author_email = 'greg@gregstoll.com',
       description = 'Converts float to hex and back',
       long_description=open('README.md').read(),
       #long_description_content_type='text/markdown',
       license='Python Software Foundation License',
       classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications :: Modbus',
          ],
       ext_modules = [FloatToHexModule]
       )
