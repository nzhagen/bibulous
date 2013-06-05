#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# See the LICENSE.rst file for licensing information.

from __future__ import unicode_literals, print_function, division     ## for Python3 compatibility
import string
import re
import os
import sys
import pdb          ## put "pdb.set_trace()" at any place you want to interact with pdb
import bibulous


## ==================================================================================================

if (__name__ == '__main__'):
    print(sys.argv)

    try:
        auxfile = sys.argv[2]
        authorstr = sys.argv[3]
        outputfile = sys.argv[4]
    except getopt.GetoptError as err:
        print(str(err)) ## will print something like "option -a not recognized"
        print('usage:')
        print('>>> python bibulous-authorextract.py auxfile "author name in quotes" outfile ...')
        print('if "file1" has a ".aux" extension, then it is assumed that the file contains the '
              'locations of the ".bib" files.')
        print('if "file1" has a ".bib" extension, then it is assumed to be a ".bib" database '
              'filename (as are all subsequent files).')
        sys.exit(2)

    bibdata = Bibdata(auxfile)
    bibextract_filename = outputfile[:-4] + '-authorextract.bib'
    print('Writing BIB author extract file = ' + outputfile)
    write_authorextract(authorstr, outputfile, debug=False)
