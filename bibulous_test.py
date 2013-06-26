#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# See the LICENSE.rst file for licensing information.
'''
    Bibulous_test.py is a script which runs through the entire Bibulous regression testing suite.

    The basic approach of the tests is as follows:
    (1) Once a change is made to the code (to fix a bug or add functionality), the writer should
        add an entry to the /test/test1.bib file, where the "entrytype" gives an indication of
        what the test is for. For example, the entry in the BIB file may start with
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
    (4) Add two lines to the test1_target.bbl file (one for the "bibentry" function call, and one
        for the entry contents) to say what the formatted result should look like.
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
import locale
import traceback    ## for getting full traceback info in exceptions
import pdb          ## put "pdb.set_trace()" at any place you want to interact with pdb
import difflib      ## for comparing one string sequence with another
from bibulous import Bibdata


## ==================================================================================================
def run_test1():
    '''
    Test #1 consists of a suite of single tests of options and features that are valid with the
    default template file.
    '''

    bstfiles = ('./test/test1.bst',                 ## the "default" style template must go first!
                './test/test1_force_sentence_case.bst',
                './test/test1_french_initials.bst',
                './test/test1_use_name_ties.bst',
                './test/test1_period_after_initial.bst',
                './test/test1_terse_inits.bst')
    bibfile = './test/test1.bib'
    bblfile = './test/test1.bbl'
    auxfile = './test/test1.aux'
    target_bblfile = './test/test1_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous-test1 on: ' + bibfile)
    print('The target output BBL file: ' + target_bblfile)
    print('The testing template files are: ' + bstfiles[0])
    for b in bstfiles[1:]:
        print('                                ' + b)
    print('The current working directory is: ' + os.getcwd())
    print('The actual output BBL file: ' + bblfile)

    bibobj = Bibdata([bibfile,auxfile,bblfile,bstfiles[0]])
    bibobj.write_bblfile(write_preamble=True, write_postamble=False, bibsize='XX')
    bstfiles = bstfiles[1:]

    for bstfile in bstfiles:
        auxfile = bstfile[:-4] + '.aux'
        print('Reading ' + bstfile + ' and ' + auxfile)
        ## Delete the old citekeys so that the new test contains only the new keys.
        bibobj.citedict = {}
        bibobj.parse_auxfile(auxfile)

        ## For the style templates, always use the default templates first and the
        ## specific test template second --- this allows each test template to be
        ## very simple (only the differences from the default need to be used).
        if (bstfile != bstfiles[0]):
            bibobj.parse_bstfile(bstfiles[0])
        bibobj.parse_bstfile(bstfile)

        write_postamble = (bstfile == bstfiles[-1])
        bibobj.write_bblfile(write_preamble=False, write_postamble=write_postamble)

    return(bblfile, target_bblfile)

## =============================
def run_test2():
    '''
    Test #2 loads a number of large .bib database files to put the BibTeX parser and the BBL file
    writer through a comprehensive set of conditions. Every entry in the BIB files is written to
    the output BBL file to test as much of the processing chain as possible.

    Rather than checking the output against a target file, this test really just makes sure that
    no exceptions are emitted when processing the entire database through the full chain of
    functions.
    '''

    bstfile = './test/test2.bst'
    bibfiles = ['./test/master.bib',   './test/journal.bib',   './test/amstat.bib',
               './test/cccuj2000.bib', './test/gutenberg.bib', './test/onlinealgs.bib',
               './test/python.bib',    './test/random.bib',    './test/sciam2000.bib',
               './test/template.bib',  './test/thiruv.bib',    './test/benfords-law.bib',
               './test/texstuff.bib',  './test/karger.bib']
    bblfile = './test/test2.bbl'
    auxfile = './test/test2.aux'

    print('\n' + '='*75)
    print('Running Bibulous-test2 on: ' + bibfiles[0])
    for b in bibfiles[1:]:
        print('                           ' + b)
    print('The testing template file is: ' + bstfile)
    print('The current working directory is: ' + os.getcwd())
    print('The actual output BBL file: ' + bblfile)

    filenames = bibfiles + [bblfile,bstfile]
    bibobj = Bibdata(filenames)

    ## Build a large citation dictionary using all of the bibliography database entries.
    citedict = {k:i for i,k in enumerate(bibobj.bibdata.keys())}
    if ('abbrev' in citedict): del citedict['abbrev']
    if ('preamble' in citedict): del citedict['preamble']
    bibobj.citedict = citedict
    f = open(auxfile, 'w')
    for c in citedict:
        f.write('\\citation{' + c + '}\n')
    f.write('\\bibdata{')
    for b in bibfiles[:-1]:
        f.write(os.path.basename(b) + ',')
    f.write(os.path.basename(bibfiles[-1]) + '}\n')
    f.write('\\bibstyle{test2.bst}\n')
    f.close()
    bibobj.write_bblfile()

    return(bblfile)

## =============================
def run_test3():
    '''
    Test #3 tests that the "authorextract" and "citeextract" methods function correctly.
    '''

    auxfile = './test/test2.aux'        ## re-use the huge database
    authorstr = 'John W. Tukey'
    outputfile1 = './test/test3_authorextract.bib'
    targetfile1 = './test/test3_authorextract_target.bib'

    print('\n' + '='*75)
    print('Running Bibulous-test3 for author "' + authorstr + '"')

    bibobj = Bibdata(auxfile)
    print('Writing BIB author extract file = ' + outputfile1)
    bibobj.write_authorextract(authorstr, outputfile1, debug=False)

    ## Next do the cite-extract check.
    auxfile = './test/test3_citeextract.aux'
    outputfile2 = './test/test3_citeextract.bib'
    targetfile2 = './test/test3_citeextract_target.bib'
    print('Writing BIB author extract file = ' + outputfile2)

    ## Delete the old citekeys so that the new test contains only the new keys.
    bibobj.citedict = {}
    bibobj.parse_auxfile(auxfile)
    bibobj.write_citeextract(outputfile2, debug=False)

    outputfiles = [outputfile1, outputfile2]
    targetfiles = [targetfile1, targetfile2]

    return(outputfiles, targetfiles)

## ==================================================================================================
def run_test4():
    '''
    Test #4 checks the operation of generating citation keys.
    '''

    ## Although three of these files were copied from "test1", it is a bad idea to use the "test1.*"
    ## files here because any changes to test1 would then require changes to the test4_target.bbl
    ## as well.
    bstfile = './test/test4.bst'
    bibfile = './test/test4.bib'
    bblfile = './test/test4.bbl'
    auxfile = './test/test4.aux'
    target_bblfile = './test/test4_target.bbl'

    ## The default locale will be US english. Ironically, the locale argument needs to use an ASCII
    ## string, and since the default string encoding here is Unicode, we have to re-encode it
    ## manually. Later below, we will try some other locale settings.
    thislocale = locale.setlocale(locale.LC_ALL,'en_US.UTF8'.encode('ascii','replace'))

    ## Need to make a list of all the citation order options we want to try. Skip "citenum" since
    ## that is the default, and so has been tested already.
    citation_order_options = ['citekey', ## citekey
                              'nyt',     ## uses the first author's last name, the year, and then the title
                              'alpha',   ## uses three letters of author's last name plus last two numbers in the year
                              'plain',   ## (same as nyt)
                              'nty',     ## name-title-year
                              'nyvt',    ## name-year-volume-title
                              'anyt',    ## labelalpha-name-year-title
                              'anyvt',   ## labelalpha-name-year-volume-title
                              'ynt',     ## year-name-title
                              'ydnt']    ## year-name-title: in descending order

    print('\n' + '='*75)
    print('Running Bibulous-test4 on: ' + bibfile)
    print('The target output BBL file: ' + target_bblfile)
    print('The testing template file is: ' + bstfile)
    print('The current working directory is: ' + os.getcwd())
    print('The actual output BBL file: ' + bblfile)

    bibobj = Bibdata([bibfile,auxfile,bblfile,bstfile])
    bibobj.locale = thislocale
    bibobj.bibdata['preamble'] = '\n'
    #bibobj.debug = True     ## turn on debugging for citekey printing

    for order in citation_order_options:
        ## Delete the old citekeys so that the new test contains only the new keys.
        print('Setting citation_order = ' + order)
        bibobj.citedict = {}
        bibobj.options['citation_order'] = order
        bibobj.parse_auxfile(auxfile)      ## this generates the citations
        write_preamble = (order == citation_order_options[0])
        write_postamble = (order == citation_order_options[-1])
        bibobj.write_bblfile(write_preamble=write_preamble, write_postamble=False)

        filehandle = open(bblfile, 'a')
        filehandle.write('\n\n')
        filehandle.close()

    ## Delete the old citekeys so that the new test contains only the new keys.
    print('Setting option sort_case = True')
    bibobj.citedict = {}
    bibobj.options['citation_order'] = 'nyt'
    bibobj.options['sort_case'] = True
    bibobj.parse_auxfile(auxfile)      ## this generates the citations
    bibobj.write_bblfile(write_preamble=False, write_postamble=False)
    filehandle = open(bblfile, 'a')
    filehandle.write('\n\n')
    filehandle.close()

    ## Delete the old citekeys so that the new test contains only the new keys.
    print('Setting option sort_with_prefix = True')
    bibobj.citedict = {}
    bibobj.options['sort_with_prefix'] = True
    bibobj.parse_auxfile(auxfile)      ## this generates the citations
    bibobj.write_bblfile(write_preamble=False, write_postamble=True)
    filehandle = open(bblfile, 'a')
    filehandle.write('\n\n')
    filehandle.close()

    return(bblfile, target_bblfile)

## =============================
def run_test5():
    '''
    Test #5 flexes the Python API.
    '''

    auxfile = './test/test5.aux'
    bblfile = './test/test5.bbl'
    targetfile = './test/test5_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous-test5')

    bibobj = Bibdata(auxfile, debug=False)
    bibobj.write_bblfile(write_preamble=True, write_postamble=True)

    return(bblfile, targetfile)

## =============================
def check_file_match(testnum, outputfile, targetfile):
    if not isinstance(outputfile, list):
      outputfile = [outputfile]
    if not isinstance(targetfile, list):
        targetfile = [targetfile]

    alldiffs = []
    for i in range(len(outputfile)):
        file1 = outputfile[i]
        file2 = targetfile[i]
        print('COMPARING FILES "' + file1 + '" and "' + file2 + '" ...')

        ## Load the actual output BBL file and the target BBL file (the former says what we got; the
        ## latter says what we *should* get). Load each into strings and calculate their difference.
        foutput = open(file1, 'rU')
        ftarget = open(file2, 'rU')

        outputlines = foutput.readlines()
        targetlines = ftarget.readlines()

        foutput.close()
        ftarget.close()

        #diffobj = difflib.ndiff(outputlines, targetlines, lineterm='')
        diffobj = difflib.unified_diff(outputlines, targetlines, lineterm='')
        difflist = list(diffobj)
        if (len(difflist) > 1):
            alldiffs.extend(difflist)

    if (len(alldiffs) < 2):
        print('TEST #%i PASSED' % testnum)
    else:
        print('TEST #%i FAILED. FILE DIFFERENCES:' % testnum)
        for line in alldiffs: print(line, end='')

    return(difflist)


## ==================================================================================================
if (__name__ == '__main__'):
    ## Run test #1.
    (outputfile, targetfile) = run_test1()
    check_file_match(1, outputfile, targetfile)

#    ## Run test #2.
#    outputfile = run_test2()
#    print('Test #2 PASSED')
#
#    ## Run test #3.
#    (outputfile, targetfile) = run_test3()
#    check_file_match(3, outputfile, targetfile)
#
#    ## Run test #4.
#    (outputfile, targetfile) = run_test4()
#    check_file_match(4, outputfile, targetfile)

    ## Run test #5.
    (outputfile, targetfile) = run_test5()
    check_file_match(5, outputfile, targetfile)

    print('DONE')

