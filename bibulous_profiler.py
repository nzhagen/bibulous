from __future__ import unicode_literals, print_function, division     ## for Python3 compatibility
import cProfile
from bibulous import Bibdata

## =================================================================================================
def run_test1():
    auxfile = './test/test1.aux'
    bibobj = Bibdata(auxfile, disable=[9,17])
    bibobj.write_bblfile(write_preamble=True, write_postamble=True, bibsize='ZZ')
    return

## =================================================================================================
## =================================================================================================

if (__name__ == '__main__'):
    #(outputfile, targetfile) = run_test1()
    cProfile.run('run_test1()')

