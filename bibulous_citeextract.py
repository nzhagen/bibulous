#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# See the LICENSE.rst file for licensing information.

from __future__ import unicode_literals, print_function, division     ## for Python3 compatibility
import sys
import getopt
from bibulous import Bibdata

## ==================================================================================================

if (__name__ == '__main__'):
    print(sys.argv)

    try:
        auxfile = sys.argv[1]
        outputfile = sys.argv[2]
    except getopt.GetoptError as err:
        print(str(err)) ## will print something like "option -a not recognized"
        print('usage:')
        print('>>> python bibulous-citeextract.py auxfile.aux output_file.bib')
        print('"auxfile.aux" contains the citation keys to extract and the names of the .bib '
              'database files.')
        print('"output_file.bib" is the bibliography database containing the exported entries.')
        sys.exit(2)

    print('Writing citation extract BIB file = ' + outputfile)
    bibdata = Bibdata(auxfile, culldata=False)
    bibdata.write_citeextract(outputfile, debug=False)
