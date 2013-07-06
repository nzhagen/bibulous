#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# See the LICENSE.rst file for licensing information.

from __future__ import unicode_literals, print_function, division     ## for Python3 compatibility
import string
import re
import os
import sys
import getopt
import pdb          ## put "pdb.set_trace()" at any place you want to interact with pdb
from bibulous import Bibdata


## ==================================================================================================

if (__name__ == '__main__'):
    print(list(sys.argv))

    try:
        auxfile = sys.argv[1]
        authorstr = sys.argv[2]
        if (len(sys.argv) > 2):
            outputfile = sys.argv[3]
        else:
            outputfile = auxfile[:-4] + '_authorextract.bib'
    except getopt.GetoptError as err:
        print(str(err)) ## will print something like "option -a not recognized"
        print('usage:')
        print('>>> python bibulous-authorextract.py auxfile "author name in quotes" outfile ...')
        print('if "file1" has a ".aux" extension, then it is assumed that the file contains the '
              'locations of the ".bib" files.')
        print('if "file1" has a ".bib" extension, then it is assumed to be a ".bib" database '
              'filename (as are all subsequent files).')
        sys.exit(2)

    bibdata = Bibdata(auxfile, culldata=False)
    print('Writing BIB author extract file = ' + outputfile)
    bibdata.write_authorextract(authorstr, outputfile, debug=False)
