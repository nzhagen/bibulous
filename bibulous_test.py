#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# See the LICENSE.rst file for licensing information.
'''
    Bibulous_test.py is a script which runs through the entire Bibulous regression testing suite.

    The basic approach of the tests is as follows:
    (1) Once a change is made to the code (to fix a bug or add functionality), the writer should add an entry to the
        /test/test1.bib file, where the "entrytype" gives an indication of what the test is for. For example, the entry
        in the BIB file may start with
                @test_initialize1{...
        and provide an "author" field where one or more authors have names which the code for generating initials can
        potentially break is not written carefully. Include a 1-line comment about the purpose of the entry as well.
    (2) If this is something which can be checked with normal options settings, then add a corresponding line in the BST
        file defining how that new entrytype ("test_initialize1") should be formatted. If different options settings are
        needed, then a new BST file is needed. To make this, copy the "test1.bst" file, remove the entrytype definitions
        (you can keep them, but they would be redundant), and change the options to the needed settings. Then add a line
        in this file to define the entrytype template.
    (3) Add a line "\citation{key}" to the AUX file where "key" is the key given in the new entry of the BIB file you
        just put in (e.g. "test_initialize1")
    (4) Add two lines to the test1_target.bbl file (one for the "bibentry" function call, and one for the entry
        contents) to say what the formatted result should look like.
    (5) Finally, run this script to check the result. This script will load the modified BIB and BST files and will
        write out a formatted BBL file "test1.bbl". It will then try to run a "diff" program on these two files to see
        if there are any differences between the target and actual output BBL files.
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
import getopt
from bibulous import Bibdata


## =================================================================================================
def run_test1():
    '''
    Test #1 consists of a suite of single tests of options and features that are valid with the default template file.
    '''

    bblfile = './test/test1.bbl'
    auxfile = './test/test1.aux'
    target_bblfile = './test/test1_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous Test #1')

    bibobj = Bibdata(auxfile, disable=[9,17])
    bibobj.write_bblfile(write_preamble=True, write_postamble=True, bibsize='ZZ')

    return(bblfile, target_bblfile)

## =================================================================================================
def run_test2():
    '''
    Test #2 loads a number of large .bib database files to put the BibTeX parser and the BBL file writer through a
    comprehensive set of conditions. Every entry in the BIB files is written to the output BBL file to test as much
    of the processing chain as possible.

    Rather than checking the output against a target file, this test really just makes sure that no exceptions are
    emitted when processing the entire database through the full chain of functions.
    '''

    bibfiles = ['./test/master.bib',    './test/journal.bib',    './test/amstat.bib',   './test/cccuj2000.bib',
                './test/gutenberg.bib', './test/onlinealgs.bib', './test/python.bib',   './test/random.bib',
                './test/sciam2000.bib', './test/template.bib',   './test/thiruv.bib',   './test/benfords-law.bib',
                './test/texstuff.bib',  './test/karger.bib']
    bblfile = './test/test2.bbl'
    auxfile = './test/test2.aux'

    print('\n' + '='*75)
    print('Running Bibulous Test #2')

    ## If no excepts are raised when reading the BIB file or writing the BBL file, then the test passes.
    try:
        bibobj = Bibdata(auxfile, disable=[4,6,9,11,18,20,21,25,32,33])
        bibobj.write_bblfile()
        result = True
        print('TEST #2 PASSED')
    except getopt.GetoptError as err:
        print('Error encountered: ' + err)
        result = False
        print('TEST #2 FAILED.')

    return(result)

## =================================================================================================
def run_test3():
    '''
    Test #3 tests that the "authorextract" method functions correctly.
    '''

    auxfile = './test/test2.aux'        ## re-use the huge database
    authorstr = 'John W. Tukey'
    outputfile = './test/test3_authorextract.bib'
    targetfile = './test/test3_authorextract_target.bib'

    print('\n' + '='*75)
    print('Running Bibulous Test #3 for author "' + authorstr + '"')

    bibobj = Bibdata(auxfile, disable=[4,9,21,32,33])
    #bibobj.debug = True
    bibobj.write_authorextract(authorstr, outputfile)

    return(outputfile, targetfile)

## =================================================================================================
def run_test4():
    '''
    Test #4 checks the operation of generating citation keys.
    '''

    ## Although three of these files were copied from "test1", it is a bad idea to use the "test1.*" files here because
    ## any changes to test1 would then require changes to the test4_target.bbl as well.
    bblfile = './test/test4.bbl'
    auxfile = './test/test4.aux'
    target_bblfile = './test/test4_target.bbl'

    ## The default locale will be US english. Ironically, the locale argument needs to use an ASCII string, and since
    ## the default string encoding here is Unicode, we have to re-encode it manually. Later below, we will try some
    ## other locale settings.
    thislocale = locale.setlocale(locale.LC_ALL,'en_US.UTF8'.encode('ascii','replace'))

    ## Need to make a list of all the citation sort options we want to try. Skip "citenum" since that is the default,
    ## and so has been tested already.
    sortkeys = ['<citekey>',
                '[<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear>|<year>|][<sorttitle>|<title>]',
                '[<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sorttitle>|<title>][<sortyear>|<year>|]',
                '[<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear>|<year>|]<volume>[<sorttitle>|<title>]',
                '[<alphalabel>][<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear>|<year>|][<sorttitle>|<title>]',
                '[<alphalabel>][<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear>|<year>|]<volume>[<sorttitle>|<title>]',
                '[<sortyear>|<year>][<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sorttitle>|<title>]',
                '-[<sortyear>|<year>][<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sorttitle>|<title>]',
                '<author_or_editor.uniquify(num)>']

    print('\n' + '='*75)
    print('Running Bibulous Test #4')

    bibobj = Bibdata(auxfile, disable=[9])
    bibobj.locale = thislocale
    bibobj.bibdata['preamble'] = '\n'
    #bibobj.debug = True     ## turn on debugging for citekey printing

    for sortkey in sortkeys:
        ## Delete the old citekeys so that the new test contains only the new keys.
        print('Setting sortkey = ' + sortkey)
        filehandle = open(bblfile, 'a')
        filehandle.write('%% SETTING SORTKEY = ' + sortkey + '\n')
        filehandle.close()

        bibobj.citedict = {}
        bibobj.sortdict = {}
        bibobj.specials['sortkey'] = sortkey
        bibobj.parse_auxfile(auxfile)      ## this generates the citations
        write_preamble = (sortkey == sortkeys[0])
        bibobj.write_bblfile(write_preamble=write_preamble, write_postamble=False, bibsize='ZZZ')

        filehandle = open(bblfile, 'a')
        filehandle.write('\n\n')
        filehandle.close()

    ## Delete the old citekeys so that the new test contains only the new keys.
    print('Setting option sort_case = True')
    filehandle = open(bblfile, 'a')
    filehandle.write('%% SETTING SORTKEY = [<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear>|<year>][<sorttitle>|<title>]\n')
    filehandle.close()

    bibobj.citedict = {}
    bibobj.sortdict = {}
    bibobj.specials['sortkey'] = '[<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear>|<year>][<sorttitle>|<title>]'
    bibobj.options['sort_case'] = True
    bibobj.parse_auxfile(auxfile)      ## this generates the citations
    bibobj.write_bblfile(write_preamble=False, write_postamble=True)
    filehandle = open(bblfile, 'a')
    filehandle.write('\n\n')
    filehandle.close()

    return(bblfile, target_bblfile)

## =================================================================================================
def run_test5():
    '''
    Test #5 flexes the Python API.
    '''

    auxfile = './test/test5.aux'
    bblfile = './test/test5.bbl'
    targetfile = './test/test5_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous Test #5')

    bibobj = Bibdata(auxfile, disable=[9], debug=False)
    bibobj.write_bblfile(write_preamble=True, write_postamble=True)

    return(bblfile, targetfile)

## =================================================================================================
def run_test6():
    '''
    Test #6 makes sure to raise an exception when attempting to load a BibTeX-format BST file.
    '''

    auxfile = './test/test6.aux'
    bstfile = './test/test6.bst'

    print('\n' + '='*75)
    print('Running Bibulous Test #6')

    try:
        bibobj = Bibdata([auxfile, bstfile], debug=False, disable=[8,9])
        result = False
        print('TEST #6 FAILED')
    except ImportError, arg:
        result = True
        print('TEST #6 PASSED.')

    return(result)

## =================================================================================================
def run_test7():
    '''
    Test #7 checks the operation of generating reference list labels.
    '''

    ## Although three of these files were copied from "test1", it is a bad idea to use the "test1.*" files here because
    ## any changes to test1 would then require changes to the test7_target.bbl as well.
    bblfile = './test/test7.bbl'
    auxfile = './test/test7.aux'
    target_bblfile = './test/test7_target.bbl'

    ## The default locale will be US english. Ironically, the locale argument needs to use an ASCII string, and since
    ## the default string encoding here is Unicode, we have to re-encode it manually. Later below, we will try some
    ## other locale settings.
    thislocale = locale.setlocale(locale.LC_ALL,'en_US.UTF8'.encode('ascii','replace'))

    ## Need to make a list of all the citation label options we want to try. Skip "citenum" since that is the default,
    ## and so has been tested already.
    citelabels = ['<citekey>',
                  '[<authorlist.0.last>|<editorlist.0.last>|]-<year>',
                  '<citealpha>',
                  '[<authorlist.0.last>|<editorlist.0.last>|], <year>',
                  '[<authorlist.0.last>|<editorlist.0.last>|] (<year>)']

    print('\n' + '='*75)
    print('Running Bibulous Test #7')

    #bibobj = Bibdata([bibfile,auxfile,bblfile,bstfile], disable=[9])
    bibobj = Bibdata(auxfile, disable=[9])
    bibobj.locale = thislocale
    bibobj.bibdata['preamble'] = '\n'
    #bibobj.debug = True     ## turn on debugging for citekey printing

    for citelabel in citelabels:
        ## Delete the old citekeys so that the new test contains only the new keys.
        print('Setting citation_label = ' + citelabel)
        bibobj.citedict = {}
        bibobj.specials['citelabel'] = citelabel
        bibobj.parse_auxfile(auxfile)      ## this generates the citations
        write_preamble = (citelabel == citelabels[0])
        write_postamble = (citelabel == citelabels[-1])
        bibobj.write_bblfile(write_preamble=write_preamble, write_postamble=write_postamble)

        filehandle = open(bblfile, 'a')
        filehandle.write('\n\n')
        filehandle.close()

    return(bblfile, target_bblfile)

## =================================================================================================
def run_test8():
    '''
    Test #8 tests Bibulous' ability to generate glossaries, symbol lists, and acronym lists.
    '''

    texfile = './test/test8.tex'
    bstfile = './test/test8.bst'
    bibfile = './test/test8.bib'
    bblfile = './test/test8.bbl'
    auxfile = './test/test8.aux'
    target_bblfile = './test/test8_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous Test #8')

    #bibobj = Bibdata([texfile,bibfile,auxfile,bblfile,bstfile], debug=False)
    bibobj = Bibdata(auxfile, debug=False)
    bibobj.write_bblfile()

    return(bblfile, target_bblfile)

## =================================================================================================
def run_test9():
    '''
    Test #9 is a pltform for running conditions in which the entire database needs to be re-read with each test.
    '''

    bstfile =  ['./test/test9_case_sensitive_fieldnames.bst']
    bibfiles = ['./test/test9_case_sensitive_fieldnames.bib']
    auxfiles = ['./test/test9_case_sensitive_fieldnames.aux']
    bblfile = './test/test9.bbl'
    target_bblfile = './test/test9_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous Test #9')

    for bibfile in bibfiles:
        auxfile = bibfile[:-4] + '.aux'
        bstfile = bibfile[:-4] + '.bst'
        print('Reading ' + bibfile + ', ' + bstfile + ', and ' + auxfile)
        bibobj = Bibdata([bibfile,auxfile,bblfile,bstfile], disable=[9])

        ## Note: you have to parse the bibfile *after* reading the style options in order for this to work right!
        #bibobj.parse_bibfile(bibfile)
        write_preamble = (bibfile == bibfiles[0])
        write_postamble = (bibfile == bibfiles[-1])
        bibobj.write_bblfile(write_preamble=write_preamble, write_postamble=write_postamble)

    return(bblfile, target_bblfile)


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

        ## Load the actual output BBL file and the target BBL file (the former says what we got; the latter says what
        ## we *should* get). Load each into strings and calculate their difference.
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
        test_passes = True
        print('TEST #%i PASSED' % testnum)
    else:
        test_passes = False
        print('TEST #%i FAILED. FILE DIFFERENCES:' % testnum)
        for line in alldiffs: print(line, end='')

    return(test_passes)


## ==================================================================================================
if (__name__ == '__main__'):
    suite_pass = True

    ## Run test #1.
    (outputfile, targetfile) = run_test1()
    result = check_file_match(1, outputfile, targetfile)
    suite_pass *= result

    ## Run test #2.
    result = run_test2()
    suite_pass *= result

    ## Run test #3.
    (outputfile, targetfile) = run_test3()
    result = check_file_match(3, outputfile, targetfile)
    suite_pass *= result

    ## Run test #4.
    (outputfile, targetfile) = run_test4()
    result = check_file_match(4, outputfile, targetfile)
    suite_pass *= result

    ## Run test #5.
    (outputfile, targetfile) = run_test5()
    result = check_file_match(5, outputfile, targetfile)
    suite_pass *= result

    ## Run test #6.
    result = run_test6()
    suite_pass *= result

    ## Run test #7.
    (outputfile, targetfile) = run_test7()
    result = check_file_match(7, outputfile, targetfile)
    suite_pass *= result

    ## Run test #8.
    (outputfile, targetfile) = run_test8()
    result = check_file_match(8, outputfile, targetfile)
    suite_pass *= result

    ## Run test #9.
    (outputfile, targetfile) = run_test9()
    result = check_file_match(9, outputfile, targetfile)
    suite_pass *= result

    if suite_pass:
        print('\n***** THE CODE PASSES ALL TESTS IN THE TESTING SUITE. *****')
    else:
        print('\n===== FAILED THE TESTING SUITE! =====')

