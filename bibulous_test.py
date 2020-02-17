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

import os
import locale
#import traceback    ## for getting full traceback info in exceptions
#import pdb          ## put "pdb.set_trace()" at any place you want to interact with pdb
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

    bibobj = Bibdata(auxfile, disable=[9,17,28,29])
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
    bstfile = './test/test4.bst'
    auxfile = './test/test4.aux'
    target_bblfile = './test/test4_target.bbl'

    ## The default locale will be US english. Later below, we will try testing some other locale settings.
    if (os.name == 'posix'):
        thislocale = locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    elif (os.name == 'nt'):
        thislocale = locale.setlocale(locale.LC_ALL, 'usa_usa')

    ## Need to make a list of all the citation sort options we want to try. Skip "citenum" since that is the default,
    ## and so has been tested already. Note: In the "uniquify" example below, the .upper() operator is needed to force the
    ## code to see 'b' and 'B' as being the same (and thus need a unique ending) when case-indep. sorting is being used.
    presortkeys = ['<citekey>',
                   '[<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear.zfill(4)>|<year.zfill(4)>|][<sorttitle>|<title>]<citekey>',
                   '[<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sorttitle>|<title>][<sortyear.zfill(4)>|<year.zfill(4)>|]<citekey>',
                   '[<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear.zfill(4)>|<year.zfill(4)>|]<volume>[<sorttitle>|<title>]<citekey>',
                   '[<alphalabel>][<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear.zfill(4)>|<year.zfill(4)>|][<sorttitle>|<title>]<citekey>',
                   '[<alphalabel>][<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear.zfill(4)>|<year.zfill(4)>|]<volume>[<sorttitle>|<title>]<citekey>',
                   '[<sortyear.zfill(4)>|<year.zfill(4)>][<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sorttitle>|<title>]<citekey>',
                   '[<sortyear.zfill(4)>|<year.zfill(4)>][<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sorttitle>|<title>]<citekey>',
                   #'<author_or_editor.initial().upper().uniquify(num)>',
                   '[<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear.zfill(4)>|<year.zfill(4)>][<sorttitle>|<title>]<citekey>']
    sortkeys = ['<presortkey.purify().lower().compress()>',
                '<presortkey.purify().lower().compress()>',
                '<presortkey.purify().lower().compress()>',
                '<presortkey.purify().lower().compress()>',
                '<presortkey.purify().lower().compress()>',
                '<presortkey.purify().lower().compress()>',
                '<presortkey.purify().lower().compress()>',
                '<presortkey.purify().lower().compress()>',
                #'<presortkey.purify().lower().compress()>',
                '<presortkey.purify().compress()>']              ## do not use .lower() here, in order to test sorting *with* case sensitivity

    sort_case_options = ['False', 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'True']
    #sort_case_options = ['True', 'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True']
    sort_order_options = ['Forward', 'Forward', 'Forward', 'Forward', 'Forward', 'Forward', 'Forward', 'Reverse', 'Forward']

    print('\n' + '='*75)
    print('Running Bibulous Test #4')

    filehandle = open(bstfile, 'r')
    lines = filehandle.readlines()
    filehandle.close()

    for i in range(len(sortkeys)):
        presortkey = presortkeys[i]
        sortkey = sortkeys[i]
        sort_case_option = sort_case_options[i]
        sort_order_option = sort_order_options[i]

        ## First go into the BST file and rewrite the "sortkey" line to be the current sortkey template.
        filehandle = open(bstfile, 'w')
        for line in lines:
            if line.startswith('presortkey = '):
                filehandle.write('presortkey = ' + presortkey + '\n')
            elif line.startswith('sortkey = '):
                filehandle.write('sortkey = ' + sortkey + '\n')
            elif line.startswith('sort_case = '):
                filehandle.write('sort_case = ' + sort_case_option + '\n')
            elif line.startswith('sort_order = '):
                filehandle.write('sort_order = ' + sort_order_option + '\n')
            else:
                filehandle.write(line)
        filehandle.close()

        bibobj = Bibdata(auxfile, disable=[9], silent=(i>0))
        bibobj.locale = thislocale
        bibobj.bibdata['preamble'] = '\n\n%% SETTING PRESORTKEY = ' + presortkey
        bibobj.bibdata['preamble'] += '\n%% SETTING SORTKEY = ' + sortkey
        #bibobj.debug = True     ## turn on debugging for citekey printing
        print('Setting PRESORTKEY = ' + presortkey)
        print('Setting SORTKEY = ' + sortkey)

        write_preamble = (presortkey == presortkeys[0])
        write_postamble = (presortkey == presortkeys[-1])
        if not write_preamble:
            filehandle = open(bblfile, 'a')
            filehandle.write('\n\n%% SETTING PRESORTKEY = ' + presortkey + '\n')
            filehandle.write('%% SETTING SORTKEY = ' + sortkey + '\n')
            #if (sort_case_option == 'True'): filehandle.write('%% SETTING SORT_CASE = True\n')
            if (sort_order_option == 'Reverse'): filehandle.write('%% SETTING SORT_ORDER = Reverse\n')
            filehandle.close()

        bibobj.write_bblfile(write_preamble=write_preamble, write_postamble=write_postamble, bibsize='ZZZ')

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
        Bibdata([auxfile, bstfile], debug=False, disable=[8,9])
        result = False
        print('TEST #6 FAILED')
    except ImportError:
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
    bstfile = './test/test7.bst'
    auxfile = './test/test7.aux'
    target_bblfile = './test/test7_target.bbl'

    ## The default locale will be US english. Later below, we will try testing some other locale settings.
    if (os.name == 'posix'):
        thislocale = locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    elif (os.name == 'nt'):
        thislocale = locale.setlocale(locale.LC_ALL, 'usa_usa')

    ## Need to make a list of all the citation label options we want to try. Skip "citenum" since that is the default,
    ## and so has been tested already.
    citelabels = ['<citekey>',
                  '[<authorlist.0.last>|<editorlist.0.last>|]-<year>',
                  '<citealpha>',
                  '[<authorlist.0.last>|<editorlist.0.last>|], <year>',
                  '[<authorlist.0.last>|<editorlist.0.last>|] (<year>)',
                  '(<citealnum>)']

    print('\n' + '='*75)
    print('Running Bibulous Test #7')

    filehandle = open(bstfile, 'r')
    lines = filehandle.readlines()
    filehandle.close()

    for i in range(len(citelabels)):
        citelabel = citelabels[i]

        ## First go into the BST file and rewrite the "citelabel" line to be the current sortkey template.
        filehandle = open(bstfile, 'w')
        for line in lines:
            if line.startswith('citelabel = '):
                filehandle.write('citelabel = ' + citelabel + '\n')
            else:
                filehandle.write(line)
        filehandle.close()

        bibobj = Bibdata(auxfile, disable=[9], silent=(i>0))
        bibobj.locale = thislocale
        bibobj.bibdata['preamble'] = '\n\n%% SETTING CITELABEL = ' + citelabel
        #bibobj.debug = True     ## turn on debugging for citekey printing

        print('Setting citation_label = ' + citelabel)
        write_preamble = (citelabel == citelabels[0])
        write_postamble = (citelabel == citelabels[-1])
        if not write_preamble:
            filehandle = open(bblfile, 'a')
            filehandle.write('\n\n%% SETTING SETTING CITELABEL = ' + citelabel + '\n')
            filehandle.close()

        bibobj.write_bblfile(write_preamble=write_preamble, write_postamble=write_postamble)

    return(bblfile, target_bblfile)

## =================================================================================================
def run_test8():
    '''
    Test #8 tests Bibulous' ability to generate glossaries, symbol lists, and acronym lists.
    '''

    bblfile = './test/test8.bbl'
    auxfile = './test/test8.aux'
    target_bblfile = './test/test8_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous Test #8')

    bibobj = Bibdata(auxfile, debug=False)
    bibobj.write_bblfile()

    return(bblfile, target_bblfile)

## =================================================================================================
def run_test9():
    '''
    Test #9 is a platform for running conditions in which the entire database needs to be re-read with each test.
    '''

    auxfiles = ['./test/test9_case_sensitive_fieldnames.aux',
                './test/test9_italian_name_separator.aux']
    bblfile = './test/test9.bbl'
    target_bblfile = './test/test9_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous Test #9')

    for auxfile in auxfiles:
        bibobj = Bibdata(auxfile, disable=[9], silent=(auxfile != auxfiles[0]))
        bibobj.filedict['bbl'] = bblfile
        write_preamble = (auxfile == auxfiles[0])
        write_postamble = (auxfile == auxfiles[-1])
        bibobj.write_bblfile(write_preamble=write_preamble, write_postamble=write_postamble)
        print('')

    return(bblfile, target_bblfile)

## =================================================================================================
def run_test10():
    '''
    Test #10 checks Bibulous' ability to sort numbers correctly (i.e. "human" sorting, so that "10" goes after, not
    before, "2").
    '''

    bblfile = './test/test10_humansort.bbl'
    auxfile = './test/test10_humansort.aux'
    target_bblfile = './test/test10_humansort_target.bbl'

    print('\n' + '='*75)
    print('Running Bibulous Test #10')

    bibobj = Bibdata(auxfile, debug=False)
    bibobj.write_bblfile()

    return(bblfile, target_bblfile)

## =================================================================================================
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
        foutput = open(file1, 'r')
        ftarget = open(file2, 'r')

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

## =================================================================================================
## ==================================================================================================
if (__name__ == '__main__'):
    ## Note: running the test suites will generate a lot of messages, some of which are warnings. This is okay. All that
    ## matters is whether the variable "suite_pass" is True or False.
    suite_pass = True

    ## Run test #1: testing miscellaneous templates.
    (outputfile, targetfile) = run_test1()
    result = check_file_match(1, outputfile, targetfile)
    suite_pass *= result

    ## Run test #2: testing the BIB file parser.
    result = run_test2()
    suite_pass *= result

    ## Run test #3: testing the "authorextract" function.
    (outputfile, targetfile) = run_test3()
    result = check_file_match(3, outputfile, targetfile)
    suite_pass *= result

    ## Run test #4: testing the correct generation of citation keys.
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

    ## Run test #10.
    (outputfile, targetfile) = run_test10()
    result = check_file_match(10, outputfile, targetfile)
    suite_pass *= result

    if suite_pass:
        print('\n***** THE CODE PASSES ALL TESTS IN THE TESTING SUITE. *****')
    else:
        print('\n===== FAILED THE TESTING SUITE! =====')

