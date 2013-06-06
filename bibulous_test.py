#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# See the LICENSE.rst file for licensing information.
'''
    Bibulous_test.py is a script which runs through the entire suite of tests to check that the
    code is working correctly.

    The basic approach of the tests is as follows:
    (1) Once a change is made to the code (to fix a bug or add functionality), the writer should
        add an entry to the /test/test1.bib file, where the "entrytype" gives an indication of
        what the test is form. For example, the entry in the BIB file may start with
                @test_initialize1{...
        and provide an "author" field where one or more authors have names which the code for
        generating initials can potentially break is not written carefully. Include a 1-line
        comment about the purpose of the entry as well.
    (2) If this is something which can be checked with normal options settings, then add a
        corresponding line in the BST file defining how that new entrytype ("test_initialize1")
        should be formatted. If different options settings are needed, then a new BST file is
        needed. To make this, copy the "test1.bst" file, remove the entrytype definitions (you can
        keep them, but they would be redundant), and change the options to the needed settings.
        Then add a line in this file to define the entrytype template.
    (3) Add a line "\citation{key}" to the AUX file where "key" is the key given in the new entry
        of the BIB file you just put in (e.g. "test_initialize1")
    (4) Add two lines to the test1_target.bbl file to say what the formatted result should look like.
    (5) Finally, run this script to check the result. This script will load the modified BIB and
        BST files and will write out a formatted BBL file "test1.bbl". It will then try to run a
        "diff" program on these two files to see if there are any differences between the target
        and actual output BBL files.
'''

from __future__ import unicode_literals, print_function, division     ## for Python3 compatibility
import string
import re
import os
import sys
import traceback    ## for getting full traceback info in exceptions
import pdb          ## put "pdb.set_trace()" at any place you want to interact with pdb
from bibulous import Bibdata
import difflib      ## for comparing one string sequence with another


## ==================================================================================================
## Test #1 consists of various single tests of options and features.
def run_test1():
    bstfiles = ('./test/test1.bst', './test/test1_sentencecase.bst', './test/test1_frenchinitials.bst')
    bibfile = './test/test1.bib'
    bblfile = './test/test1.bbl'
    auxfile = './test/test1.aux'
    target_bblfile = './test/test1_target.bbl'

    print('')
    print('============================================================================')
    print('Running Bibulous-test1 on: ' + bibfile)
    print('The target output BBL file: ' + target_bblfile)
    print('The testing template files are: ' + bstfiles[0])
    for b in bstfiles[1:]:
        print('                                ' + b)
    print('The current working directory is: ' + os.getcwd())
    print('The actual output BBL file: ' + bblfile)

    test1bib = Bibdata([bibfile,auxfile,bblfile,bstfiles[0]])
    test1bib.write_bblfile(write_preamble=True, write_postamble=False, bibsize='XX')
    bstfiles = bstfiles[1:]

    for bstfile in bstfiles:
        auxfile = bstfile[:-4] + '.aux'
        print('Reading ' + bstfile + ' and ' + auxfile)
        ## Delete the old citekeys so that the new test contains only the new keys.
        test1bib.citedict = {}
        test1bib.parse_auxfile(auxfile)
        test1bib.parse_bstfile(bstfile, debug=False)
        write_postamble = (bstfile == bstfiles[-1])
        test1bib.write_bblfile(write_preamble=False, write_postamble=write_postamble)

    return(bblfile, target_bblfile)

## =============================
## Test #2 loads a number of large .bib database files to put the parser through a
## thorough suite of tests. It also writes every entry to a BBL file to test the
## entire process chain.
def run_test2():
    bstfile = './test/test2.bst'
    bibfiles = ['./test/journal.bib', './test/amstat.bib', './test/benfords-law.bib',
               './test/cccuj2000.bib', './test/gutenberg.bib', './test/onlinealgs.bib',
               './test/python.bib', './test/random.bib', './test/sciam2000.bib',
               './test/template.bib', './test/thiruv.bib']
    bblfile = './test/test2.bbl'
    target_bblfile = './test/test2_target.bbl'

    print('')
    print('============================================================================')
    print('Running Bibulous-test2 on: ' + bibfiles[0])
    for b in bibfiles[1:]:
        print('                           ' + b)
    print('The target output BBL file: ' + target_bblfile)
    print('The testing template file is: ' + bstfile)
    print('The current working directory is: ' + os.getcwd())
    print('The actual output BBL file: ' + bblfile)

    filenames = bibfiles
    filenames.append(bblfile)
    filenames.append(bstfile)
    test2bib = Bibdata(filenames)

    ## Build a large citation dictionary using all of the bibliography database entries.
    citedict = {k:i for i,k in enumerate(test2bib.bibdata.keys())}
    if ('abbrev' in citedict): del citedict['abbrev']
    if ('preamble' in citedict): del citedict['preamble']
    test2bib.citedict = citedict
    test2bib.write_bblfile()

    return(bblfile, target_bblfile)

## =============================
def check_file_match(outputfile, targetfile):
    ## Load the actual output BBL file and the target BBL file (the former says what we got; the
    ## latter says what we *should* get). Load each into strings and calculate their difference.
    foutput = open(outputfile, 'rU')
    ftarget = open(targetfile, 'rU')

    outputlines = foutput.readlines()
    targetlines = ftarget.readlines()

    foutput.close()
    ftarget.close()

    diff = difflib.unified_diff(outputlines, targetlines, lineterm='')
    diff = list(diff)
    return(diff)


## ==================================================================================================
if (__name__ == '__main__'):
    ## Run test #1.
    (outputfile, targetfile) = run_test1()
    diff = check_file_match(outputfile, targetfile)
    if not diff:
        print('TEST #1 PASSED')
    else:
        print('TEST #1 FAILED. FILE DIFFERENCES:')
        for line in diff: print(line, end='')

    raise ValueError('')

    ## Run test #1.
    (outputfile, targetfile) = run_test2()
#    diff = check_file_match(outputfile, targetfile)
#    if not diff:
#        print('TEST #1 PASSED')
#    else:
#        print('TEST #1 FAILED. FILE DIFFERENCES:')
#        for line in diff: print(line, end='')


    print('DONE')

