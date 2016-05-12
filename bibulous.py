#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# pylint: disable-msg=C0321
# pylint: max-line-length=120
# pylint: max-module-lines=10000
# See the LICENSE.rst file for licensing information.

from __future__ import unicode_literals, print_function, division
import re
import os
import sys
import codecs       ## for importing UTF8-encoded files
import locale       ## for language internationalization and localization
import getopt       ## for getting command-line options
import copy         ## for the "deepcopy" command
import platform     ## for determining the OS of the system
#import pdb          ## put "pdb.set_trace()" at any place you want to interact with pdb
#import traceback    ## for getting full traceback info in exceptions

'''
Bibulous is a drop-in replacement for BibTeX, with the primary advantage that the bibliography
template format is compact and *very* easy to modify.

The basic program flow upon object initialization is as follows:

1. Read the `.aux` file and get the names of the bibliography databases (`.bib` files),
   the style templates (`.bst` files) to use, and the entire set of citations.
2. Read in the Bibulous style template `.bst` file as a dictionary (`bstdict`). This also
   allows us to set options for how to parse the database file(s).
3. Look for the `-extract.bib` "extracted" database file. If it exists, then read it in.
   Compare the entrykeys in the the extracted database to the citation keys in the `.aux`
   file. If any of the latter are not within the extracted database, then re-extract the
   database from the main database file. Otherwise, continue with the extracted database.
4. If the extracted database doesn't exist, or need to be replaced, then read in all of
   the bibliography database files into one long dictionary (`bibdata`), replacing any
   abbreviations with their full form. Cross-referenced data is *not* yet inserted at
   this point. That is delayed until the time of writing the BBL file in order to speed up
   parsing.
5. Now that all the information is collected, go through each citation key, find the
   corresponding entry key in `bibdata`. From the entry type, select a template from `bstdict`
   and begin inserting the variables one-by-one into the template. If any data is missing,
   check for cross-references and use crossref data to fill in missing values.
'''

#def info(type, value, tb):
#   #if (not sys.stderr.isatty() or
#   #    not sys.stdin.isatty()):
#   #    ## stdin or stderr is redirected, just do the normal thing
#   #    original_hook(type, value, tb)
#   #else:
#   if True:
#       ## a terminal is attached and stderr is not redirected, debug
#       traceback.print_exception(type, value, tb)
#       print('')
#       pdb.pm()
#       #traceback.print_stack()
#sys.excepthook = info      ## go into debugger automatically on an exception

__authors__ = 'Nathan Hagen'
__license__ = 'MIT/X11 License'
__contact__ = 'Nathan Hagen <and.the.light.shattered@gmail.com>'
__version__ = '1.3'
__all__ = ['sentence_case', 'stringsplit', 'namefield_to_namelist', 'namestr_to_namedict',
           'initialize_name', 'get_delim_levels', 'show_levels_debug', 'get_quote_levels', 'splitat', 'multisplit',
           'enwrap_nested_string', 'enwrap_nested_quotes', 'purify_string', 'latex_to_utf8',
           'search_middlename_for_prefixes', 'get_edition_ordinal', 'export_bibfile', 'parse_pagerange',
           'parse_nameabbrev', 'filter_script', 'str_is_integer', 'bib_warning', 'create_citation_alpha',
           'toplevel_split', 'get_variable_name_elements', 'get_names', 'format_namelist',
           'namedict_to_formatted_namestr', 'argsort', 'create_alphanum_citelabels','get_implicit_loop_data']


class Bibdata(object):
    '''
    Bibdata is a class to hold all data related to a bibliography database, a citation list, and a style template.

    To initialize the class, either call it with the filename of the `.aux` file containing the relevant file locations
    (for the `.bib` database files and the `.bst` template files) or simply call it with a list of all filenames to be
    used (i.e. `database_name.bib`, `style_template_name.bst` and `main_filename.aux`). The output file (the LaTeX-
    formatted bibliography) is assumed to have the same filename root as the `.aux` file, but with `.bbl` as its
    extension.

    Attributes
    ----------
    abbrevs : dict
        The list of abbreviations given in the bibliography database file(s). The dictionary keys are the \
        abbreviations, and the values are their full forms.
    bibdata : dict
        The database of bibliography entries and fields derived from parsing the bibliography database file(s).
    bstdict : dict
        The style template for formatting the bibliography. The dictionary keys are the entrytypes, with the dictionary
        values their string template.
    citedict : dict
        The dictionary of citation keys, and their corresponding numerical order of citation.
    debug : bool
        Whether to turn on debugging features.
    filedict : dict
        The ditionary of filenames associated with the bibliographic data. The dictionary consists of keys `bib`, \
        `bst`, `aux`, `tex`, and `bbl`. The first two are lists of filenames, while the others contain only a single \
        filename.
    filename : str
        (For error messages and debugging) The name of the file currently being parsed.
    i : int
        (For error messages and debugging) The line of the file currently being parsed.
    options : dict
        The dictionary containing the various option settings from the style template (BST) files.
    specials : dict
        The dictionary containing the special templates from the BST file(s).
    abbrevkey_pattern : compiled regular expression object
        The regex used to search for abbreviation keys.
    anybrace_pattern : compiled regular expression object
        The regex used to search for curly braces `{` or `}`.
    anybraceorquote_pattern : compiled regular expression object
        The regex used to search for curly braces or for double-quotes, i.e. `{`, `}`, or `"`.
    endbrace_pattern : compiled regular expression object
        The regex used to search for an ending curly brace, i.e. '}'.
    quote_pattern : compiled regular expression object
        The regex used to search for a double-quote, i.e. `"`.
    startbrace_pattern : compiled regular expression object
        The regex used to search for a starting curly brace, `{`.
    culldata : bool
        Whether to cull the database so that only cited entries are parsed. Setting this to False means that the entire \
        BIB file database will be parsed. When True, the BIB file parser will only parse those entries corresponding to \
        keys in the citedict. Setting this to True provides significant speedups for large databases.
    parse_only_entrykeys : bool
        When comparing a database file against a citation list, all we are initially interested in are the entrykeys \
        and not the data. So, in our first pass through the database, we can use this flag to skip the data and get \
        only the keys themselves.

    Methods
    -------
    parse_bibfile
    parse_bibentry
    parse_bibfield
    parse_auxfile
    parse_bstfile
    write_bblfile
    create_citation_list
    format_bibitem
    insert_crossref_data
    write_citeextract
    write_authorextract
    replace_abbrevs_with_full
    get_bibfilenames
    check_citekeys_in_datakeys
    add_crossrefs_to_searchkeys
    insert_specials
    validate_templatestr
    fillout_implicit_indices
    template_substitution
    insert_title_into_template
    remove_nested_template_options_brackets
    remove_template_options_brackets
    simplify_template_bracket
    get_variable
    get_indexed_variable
    get_indexed_vars_in_template

    Example
    -------
    bibdata = Bibdata('jobname.aux')
    bibdata.write_bblfile()
    '''

    def __init__(self, filename, disable=None, culldata=True, uselocale=None, silent=False, debug=False):
        self.debug = debug
        self.abbrevs = {'jan':'1', 'feb':'2', 'mar':'3', 'apr':'4', 'may':'5', 'jun':'6',
                        'jul':'7', 'aug':'8', 'sep':'9', 'oct':'10', 'nov':'11', 'dec':'12'}
        self.bibdata = {'preamble':''}
        self.filedict = {}          ## the dictionary containing all of the files associated with the bibliography
        self.citedict = {}          ## the dictionary containing the original data from the AUX file
        self.citelist = []          ## the list of citation keys, given in the order determined by "self.sortlist"
        self.sortlist = []          ## the (sorted) list of sorting keys
        self.bstdict = {}           ## the dictionary containing all information from template files
        self.user_script = ''       ## any user-written Python scripts go here
        self.user_variables = {}    ## any user-defined variables from the BST files
        self.culldata = culldata    ## whether to cull the database so that only cited entries are parsed
        self.searchkeys = []        ## when culling data, this is the list of keys to limit parsing to
        self.parse_only_entrykeys = False  ## don't parse the data in the database; get only entrykeys
        self.nested_templates = []  ## which templates have nested option blocks
        self.looped_templates = {} #['au','ed']  ## which templates have implicit loops
        self.implicitly_indexed_vars = ['authorname','editorname'] ## which templates have implicit indexing
        self.namelists = []         ## the namelists defined within the templates
        self.uniquify_vars = {}     ## dict containing all variables calling the "uniquify" operator
        self.keylist = []           ## "keylist" is just a temporary holding place for the citations
        self.auxfile_list = []      ## a list of *.aux files, for use when citations are inside nested files

        if (uselocale == None):
            self.locale = locale.setlocale(locale.LC_ALL,'')    ## set the locale to the user's default
        else:
            self.locale = locale.setlocale(locale.LC_ALL,uselocale)    ## set the locale to the user's default

        ## Not only do we need a dictionary for "special templates" but we also need to be able to iterate through it
        ## in the order given in the file. Thus, we have a "specials list" too.
        self.specials_list = []

        ## Put in the default special templates.
        self.specials = {}
        self.specials['authorlist'] = '<author.to_namelist()>'
        self.specials['editorlist'] = '<editor.to_namelist()>'
        self.specials['citelabel'] = '<citenum>'
        self.specials['sortkey'] = '<citenum>'
        self.specials['au'] = '<authorlist.format_authorlist()>'
        self.specials['ed'] = '<editorlist.format_editorlist()>'

        ## Temporary variables for use in error messages while parsing files.
        self.filename = ''                      ## the current filename (for error messages)
        self.i = 0                              ## counter for line in file (for error messages)

        ## On default initialization, we don't want to issue any warnings about "overwriting" the default options. So
        ## if no "default" keyword is given, then turn off warning #9.
        if (disable == None):
            self.disable = [9]
        else:
            self.disable = disable              ## the list of warning message numbers to disable

        ## Put in default options settings.
        self.options = {}
        self.options['use_abbrevs'] = True
        self.options['undefstr'] = '???'
        self.options['procspie_as_journal'] = False
        self.options['backrefstyle'] = 'none'
        self.options['backrefs'] = False
        self.options['sort_case'] = True
        self.options['bibitemsep'] = None
        self.options['allow_scripts'] = False
        self.options['case_sensitive_field_names'] = False
        self.options['use_citeextract'] = True
        self.options['etal_message'] = ', \\textit{et al.}'
        self.options['edmsg1'] = ', ed.'
        self.options['edmsg2'] = ', eds'
        self.options['replace_newlines'] = True
        self.options['sort_order'] = 'Forward'
        self.options['wrap_nested_quotes'] = False
        self.options['autocomplete_doi'] = False
        self.options['name_separator'] = 'and'

        ## These options all relate to the default name formatting (the more rigid namelist formatting that does not use
        ## the implicit indexing and implicit loop structures).
        self.options['use_firstname_initials'] = True
        self.options['namelist_format'] = 'first_name_first'
        self.options['maxauthors'] = 9
        self.options['minauthors'] = 9
        self.options['maxeditors'] = 5
        self.options['mineditors'] = 5
        self.options['use_name_ties'] = False
        self.options['terse_inits'] = False
        self.options['french_initials'] = False
        self.options['period_after_initial'] = True

        ## Compile some patterns for use in regex searches. Note that "[\-\+\*\#\$\w]" matches any alphanumeric character plus any of [~@%&-+*#$^?!=:]
        pat = r'[~@%&\-\+\*\#\$\^\?\!\=\:\w]+?'
        self.anybrace_pattern = re.compile(r'(?<!\\)[{}]', re.UNICODE)
        self.startbrace_pattern = re.compile(r'(?<!\\){', re.UNICODE)
        self.endbrace_pattern = re.compile(r'(?<!\\)}', re.UNICODE)
        self.quote_pattern = re.compile(r'(?<!\\)"', re.UNICODE)
        self.abbrevkey_pattern = re.compile(r'(?<!\\)[,#]', re.UNICODE)
        self.anybraceorquote_pattern = re.compile(r'(?<!\\)[{}"]', re.UNICODE)
        self.integer_pattern = re.compile(r'^-?[0-9]+', re.UNICODE)
        self.index_pattern = re.compile(r'(<'+pat+r'\.\d+\.'+pat+r'>)|(<'+pat+r'\.\d+>)|(<'+pat+r'\.(nN)\.'+pat+r'>)|('+pat+r'\.(nN)>)', re.UNICODE)
        self.implicit_index_pattern = re.compile(r'(<'+pat+r'\.n\.'+pat+r'>)|(<'+pat+r'\.n>)', re.UNICODE)
        self.template_variable_pattern = re.compile(r'(?<=<)\.+?(?=>)', re.UNICODE)
        self.namelist_variable_pattern = re.compile(r'(?<=<)\.+?(?=.to_namelist\(\)>)', re.UNICODE)

        ## Create an inverse dictionary for the month names --- one version will full names, and one with abbreviated
        ## names. For a Unix-based system, the month names are determined by the user's default locale. How to do this
        ## for a MS Windows system?
        self.monthnames = {}
        self.monthabbrevs = {}
        for i in range(1,13):
            if not (platform.system() == 'Windows'):
                ## The abbreviated form (i.e. 'Jan').
                self.monthabbrevs[unicode(i)] = locale.nl_langinfo(locale.__dict__['ABMON_'+unicode(i)]).title()
            elif (platform.system() == 'Windows'):
                self.monthabbrevs = {'1':'Jan', '2':'Feb', '3':'Mar', '4':'Apr', '5':'May', '6':'Jun',
                                     '7':'Jul', '8':'Aug', '9':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}

            if (platform.system() == 'Windows'):
                self.monthnames = {'1':'January', '2':'February', '3':'March', '4':'April',
                                   '5':'May', '6':'June', '7':'July', '8':'August', '9':'September',
                                   '10':'October', '11':'November', '12':'December'}
            else:
                ## The full form (i.e. 'January').
                self.monthnames[unicode(i)] = locale.nl_langinfo(locale.__dict__['MON_'+unicode(i)]).title()

        ## Get the list of filenames associated with the bibliography (AUX, BBL, BIB, TEX). Additionally, if the input
        ## "filename" contains only the AUX file, then we assume that the user wants only to parse that part if the
        ## database corresponding to the citation keys in the AUX file. This default behavior can be overriden (so that
        ## the entire database is parsed) is the optional keyword "cull_database" is set to False.
        self.get_bibfilenames(filename)
        if not self.filedict:
            return

        ## Print out some info on Bibulous and the files it is working on.
        if not silent:
            print('This is Bibulous, version ' + unicode(__version__))
            print('The current working directory is: ' + os.getcwd())
            print('The top-level TeX file: ' + unicode(self.filedict['tex']))
            print('The top-level auxiliary file: ' + unicode(self.filedict['aux']))
            print('The bibliography database file(s): ' + unicode(self.filedict['bib']))
            print('The Bibulous style template file(s): ' + unicode(self.filedict['bst']))
            print('The output formatted bibliography file: ' + unicode(self.filedict['bbl']) + '\n')

        if self.filedict['aux']:
            self.parse_auxfile(self.filedict['aux'])
            if ('*' in self.citedict):
                self.culldata = False

        ## Parsing the style file has to go *before* parsing the BIB file, so that any style options that affect the way
        ## the data is parsed can take effect.
        if self.filedict['bst']:
            for f in self.filedict['bst']:
                self.parse_bstfile(f)

        ## Now that we've parsed the BST file, we need to check the list of special templates. For the "authorlist" and
        ## "editorlist", the ordering matters! It may seem that this section is easily replaced with a simple list, but
        ## the structure here is needed in order to keep the order of items correct.
        if ('authorlist' not in self.specials_list):
            self.specials_list = ['authorlist'] + self.specials_list
        if ('editorlist' not in self.specials_list):
            self.specials_list = ['editorlist'] + self.specials_list
        if ('citelabel' not in self.specials_list):
            self.specials_list.append('citelabel')
        if ('sortkey' not in self.specials_list):
            self.specials_list.append('sortkey')
        if ('au' not in self.specials_list):
            self.specials_list.append('au')
        if ('ed' not in self.specials_list):
            self.specials_list.append('ed')

        ## Next, get the list of entrykeys in the database file(s), and compare them against the list of citation keys.
        if self.filedict['bib']:
            if self.citedict and self.options['use_citeextract'] and os.path.exists(self.filedict['extract']):
                ## Check if the extract file is complete by reading in the database keys and checking against the
                ## citation list.
                self.parse_only_entrykeys = True
                self.parse_bibfile(self.filedict['extract'])
                self.parse_only_entrykeys = False
                is_complete = self.check_citekeys_in_datakeys()
                if is_complete:
                    self.searchkeys = self.citedict.keys()
                else:
                    self.searchkeys = []
                ## Clear the bibliography database, or we will get "overwrite" errors when we parse it again below
                ## (since right now all we have are entrykeys).
                self.bibdata = {'preamble':''}
            else:
                is_complete = False

            ## If the current database is complete, then just go ahead and use it. If not, then parse the main database
            ## file(s).
            if is_complete:
                self.parse_bibfile(self.filedict['extract'])
            else:
                if self.culldata:
                    self.searchkeys = self.citedict.keys()
                for f in self.filedict['bib']:
                    self.parse_bibfile(f)
                if self.culldata:
                    self.add_crossrefs_to_searchkeys()
                if ('*' in self.citedict):
                    for i,key in enumerate(self.bibdata.keys()):
                        if (key != 'preamble'):
                            self.citedict[key] = 1 + i
                    if ('preamble' in self.citedict): del self.citedict['preamble']
                    if ('*' in self.citedict): del self.citedict['*']
                ## Write out the extracted database.
                if self.options['use_citeextract']:
                    self.write_citeextract(self.filedict['extract'])

        return

    ## =============================
    def parse_bibfile(self, filename):
        '''
        Parse a ".bib" file to generate a dictionary representing a bibliography database.

        Parameters
        ----------
        filename : str
            The filename of the .bib file to parse.
        '''

        ## Need to use the "codecs" module to handle UTF8 encoding/decoding properly. Using mode='rU' with the common
        ## "open()" file function doesn't do this probperly, though I don't know why.
        self.filename = filename
        filehandle = codecs.open(os.path.normpath(self.filename), 'r', 'utf-8')

        ## This next block parses the lines in the file into a dictionary. The tricky part here is that the BibTeX
        ## format allows for multiline entries. So we have to look for places where a line does not end in a comma, and
        ## check the following line to see if it a continuation of that line. Unfortunately, this means we need to read
        ## the whole file into memory --- not just one line at a time.
        entry_brace_level = 0

        ## The variable "entrystr" contains all of the contents of the entry between the entrytype definition "@____{"
        ## and the closing brace "}". Once we've obtained all of the (in general multiline) contents, then we hand them
        ## off to parse_bibentry() to format them.
        entrystr = ''
        entrytype = None
        self.i = 0           ## line number counter --- for error messages only
        entry_counter = 0
        abbrev_counter = 0

        for line in filehandle:
            self.i += 1

            ## Ignore empty and comment lines.
            if not line: continue
            if line.strip().startswith('%'): continue
            if line.startswith('}'):
                ## If a line *starts* with a closing brace, then assume the intent is to close the current entry.
                entry_brace_level = 0
                self.parse_bibentry(entrystr, entrytype)       ## close out the entry
                if (entrytype.lower() == 'string'):
                    abbrev_counter += 1
                elif (entrytype.lower() not in ('preamble','acronym')):
                    entry_counter += 1
                entrystr = ''
                if (line[1:].strip() != ''):
                    bib_warning('Warning 001a: line#' + unicode(self.i) + ' of "' + self.filename + '" has data outside'
                          ' of an entry {...} block. Skipping all contents until the next entry ...', self.disable)
                continue

            ## Don't strip off leading and ending whitespace until after checking if '}' begins a line (as in the block
            ## above).
            line = line.strip()

            if line.startswith('@'):
                brace_idx = line.find('{')             ## assume a form like "@ENTRYTYPE{"
                if (brace_idx == -1):
                    bib_warning('Warning 002a: open brace not found for the entry beginning on line#' + \
                         unicode(self.i) + ' of "' + self.filename + '". Skipping to next entry ...',
                         self.disable)
                    entry_brace_level = 0
                    continue
                entrytype = line[1:brace_idx].lower().strip()   ## extract string between "@" and "{"
                line = line[brace_idx+1:]
                entry_brace_level = 1

            ## If we are not currently inside an active entry, then skip the line and wait until the the next entry.
            if (entry_brace_level == 0):
                if (line.strip() != ''):
                    bib_warning('Warning 001b: line#' + unicode(self.i) + ' of "' + self.filename + '" has data ' + \
                                'outside of an entry {...} block. Skipping all contents until the next entry ...',
                                self.disable)
                continue

            ## Look if the entry ends with this line. If so, append it to "entrystr" and call the entry parser. If not,
            ## then simply append to the string and continue.
            endpos = len(line)

            for match in re.finditer(self.anybrace_pattern, line):
                if (match.group(0)[-1] == '}'):
                    entry_brace_level -= 1
                elif (match.group(0)[-1] == '{'):
                    entry_brace_level += 1
                if (entry_brace_level == 0):
                    ## If we've found the final brace, then check if there is anything after it.
                    if (line[match.end():].strip() != ''):
                        bib_warning('Warning 002b: line#' + unicode(self.i) + ' of "' + self.filename + \
                             '" has data outside of an entry {...} block. Skipping all ' + \
                             'contents until the next entry ...', self.disable)
                    endpos = match.end()
                    break

            ## If we have returned to brace level 0, then finish appending the contents and send the entire set to the
            ## parser.
            if (entry_brace_level == 0):
                entrystr += line[:endpos-1]      ## the "-1" here to remove the final closing brace
                self.parse_bibentry(entrystr, entrytype)
                if (entrytype.lower() == 'string'):
                    abbrev_counter += 1
                elif (entrytype.lower() not in ('preamble','acronym')):
                    entry_counter += 1
                entrystr = ''
            else:
                entrystr += line[:endpos] + '\n'

        filehandle.close()

        print('Found %i entries and %i abbrevs in %s' % (entry_counter, abbrev_counter, filename))
        #print('    Bibdata now has %i keys' % (len(self.bibdata) - 1))

        return

    ## =============================
    def parse_bibentry(self, entrystr, entrytype):
        '''
        Given a string representing the entire contents of the BibTeX-format bibliography entry, parse the contents and
        place them into the bibliography preamble string, the set of abbreviations, and the bibliography database
        dictionary.

        Parameters
        ----------
        entrystr : str
            The string containing the entire contents of the bibliography entry.
        entrytype : str
            The type of entry (`article`, `preamble`, etc.).
        '''

        if not entrystr:
            return

        if (entrytype == 'comment'):
            pass
        elif (entrytype == 'preamble'):
            ## In order to use the same "parse_bibfield()" function as all the other options, add a fake key onto the
            ## front of the string before calling "parse_bibfield()".
            fd = self.parse_bibfield('fakekey = ' + entrystr)
            if fd: self.bibdata['preamble'] += '\n' + fd['fakekey']
        elif (entrytype == 'string'):
            fd = self.parse_bibfield(entrystr)
            for fdkey in fd:
                if (fdkey in self.abbrevs):
                    bib_warning('Warning 032a: line#' + unicode(self.i) + ' of "' + self.filename +
                                ': the abbreviation "' + fdkey + '" = "' + self.abbrevs[fdkey] + '" is being '
                                'overwritten as "' + fdkey + '" = "' + fd[fdkey] + '"', self.disable)
            if fd: self.abbrevs.update(fd)
        elif (entrytype == 'acronym'):
            ## Acronym entrytypes have an identical form to "string" types, but we map them into a dictionary like a
            ## regular field, so we can access them as regular database entries.
            fd = self.parse_bibfield(entrystr)
            entrykey = fd.keys()[0]
            newentry = {'name':entrykey, 'description':fd[entrykey], 'entrytype':'acronym'}
            if (entrykey in self.bibdata):
                bib_warning('Warning 032b: line#' + unicode(self.i) + ' of "' + self.filename +
                            ': the acronym "' + entrykey + '" = "' + self.bibdata[entrykey] + '" is being '
                            'overwritten as "' + entrykey + '" = "' + fd[entrykey] + '"', self.disable)
            if fd: self.bibdata[entrykey] = newentry
        else:
            ## First get the entry key. Then send the remainder of the entry string to the parser.
            idx = entrystr.find(',')
            if (idx == -1) and ('\n' not in entrystr):
                bib_warning('Warning 035: the entry starting on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" provides only an entry key ("' + entrystr + '" and no item contents.', \
                     self.disable)
            elif (idx == -1):
                bib_warning('Warning 003: the entry ending on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" is does not have an "," for defining the entry key. '
                     'Skipping ...', self.disable)
                return(fd)

            ## Get the entry key. If we are culling the database (self.culldata == True) and the entry key is not among
            ## the citation keys, then exit --- we don't need to add this to the database.
            entrykey = entrystr[:idx].strip()

            ## If the entry is not among the list of keys to parse, then don't bother. Skip to the next entry to save
            ## time.
            if self.culldata and self.searchkeys and (entrykey not in self.searchkeys):
                return

            entrystr = entrystr[idx+1:]

            if not entrykey:
                bib_warning('Warning 004a: the entry ending on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" has an empty key. Ignoring and continuing ...', self.disable)
                return
            elif (entrykey in self.bibdata):
                bib_warning('Warning 004b: the entry ending on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" has the same key ("' + entrykey + '") as a previous ' + \
                     'entry. Overwriting the entry and continuing ...', self.disable)

            ## Create the dictionary for the database entry. Add the entrytype and entrykey. The latter is primarily
            ## useful for debugging, so we don't have to send the key separately from the entry itself.
            preexists = (entrykey in self.bibdata)
            self.bibdata[entrykey] = {}
            self.bibdata[entrykey]['entrytype'] = entrytype
            self.bibdata[entrykey]['entrykey'] = entrykey

            if not self.parse_only_entrykeys:
                fd = self.parse_bibfield(entrystr, entrykey)
                if preexists:
                    bib_warning('Warning 032c: line#' + unicode(self.i) + ' of "' + self.filename + ': the entry "' +
                                entrykey + '" is being overwritten with a new definition', self.disable)
                if fd: self.bibdata[entrykey].update(fd)

        return

    ## =============================
    def parse_bibfield(self, entrystr, entrykey=''):
        '''
        For a given string representing the raw contents of a BibTeX-format bibliography entry, parse the contents into
        a dictionary of key:value pairs corresponding to the field names and field values.

        Parameters
        ----------
        entrystr : str
            The string containing the entire contents of the bibliography entry.
        entrykey : str
            The key of the bibliography entry being parsed (useful for error messages).

        Returns
        -------
        fd : dict
            The dictionary of "field name" and "field value" pairs.
        '''

        entrystr = entrystr.strip()
        fd = {}             ## the dictionary for holding key:value string pairs

        while entrystr:
            ## First locate the field key.
            idx = entrystr.find('=')
            if (idx == -1):
                bib_warning('Warning 005: the entry ending on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" is an abbreviation-type entry but does not have an "=" '
                     'for defining the end of the abbreviation key. Skipping ...', self.disable)
                return(fd)

            fieldkey = entrystr[:idx].strip()
            if (fieldkey in fd):
                bib_warning('Warning 033: line#' + unicode(self.i) + ' of "' + self.filename + ': the "' + fieldkey +
                            '" field of entry "' + entrykey + '" is duplicated', self.disable)

            fieldstr = entrystr[idx+1:].strip()

            if not self.options['case_sensitive_field_names']:
                fieldkey = fieldkey.lower()

            if not fieldstr:
                entrystr = ''
                continue

            ## Next we go through the field contents, which may involve concatenating. When we reach the end of an
            ## individual field, we return the "result string" and truncate the entry string to remove the part we just
            ## finished parsing.
            resultstr = ''
            while fieldstr:
                firstchar = fieldstr[0]

                if (firstchar == ','):
                    ## Reached the end of the field, truncate the entry string return to the outer loop over fields.
                    fd[fieldkey] = resultstr
                    entrystr = fieldstr[1:].strip()
                    break
                elif (firstchar == '#'):
                    ## Reached a concatenation operator. Just skip it.
                    fieldstr = fieldstr[1:].strip()
                elif (firstchar == '"'):
                    ## Search for the content string that resolves the double-quote delimiter. Once you've found the
                    ## end delimiter, append the content string to the result string.
                    endpos = len(fieldstr)
                    entry_brace_level = 0
                    for match in re.finditer(self.anybraceorquote_pattern, fieldstr[1:]):
                        if (match.group(0)[-1] == '}'):
                            entry_brace_level -= 1
                        elif (match.group(0)[-1] == '{'):
                            entry_brace_level += 1
                        if (match.group(0)[-1] == '"') and (entry_brace_level == 0):
                            endpos = match.end()
                            break
                    resultstr += ' ' + fieldstr[1:endpos]
                    fieldstr = fieldstr[endpos+1:].strip()
                    if not fieldstr: entrystr = ''
                elif (firstchar == '{'):
                    ## Search for the endbrace that resolves the brace level. Once you've found it, add the intervening
                    ## contents to the result string.
                    endpos = len(fieldstr)
                    entry_brace_level = 1
                    for match in re.finditer(self.anybrace_pattern, fieldstr[1:]):
                        if (match.group(0)[-1] == '}'):
                            entry_brace_level -= 1
                        elif (match.group(0)[-1] == '{'):
                            entry_brace_level += 1
                        if (entry_brace_level == 0):
                            endpos = match.end()
                            break
                    resultstr += ' ' + fieldstr[1:endpos]
                    fieldstr = fieldstr[endpos+1:].strip()
                    if not fieldstr: entrystr = ''
                else:
                    ## If the fieldstr doesn't begin with '"' or '{' or '#', then the next set of characters must be an
                    ## abbreviation key. An abbrev key ends with a whitespace followed by either '#' or ',' (or the end
                    ## of the field). Anything else is a syntax error.
                    endpos = len(fieldstr)
                    end_of_field = False

                    ## The "abbrevkey_pattern" searches for the first '#' or ',' that is not preceded by a backslash. If
                    ## this pattern is found, then we've found the *end* of the abbreviation key.
                    if not re.search(self.abbrevkey_pattern, fieldstr):
                        ## If the "abbrevkey" is an integer, then it's not actually an abbreviation. Convert it to a
                        ## string and insert the number itself.
                        abbrevkey = fieldstr
                        if re.match(self.integer_pattern, abbrevkey):
                            resultstr += unicode(abbrevkey)
                        else:
                            if abbrevkey in self.abbrevs:
                                resultstr += self.abbrevs[abbrevkey].strip()
                            else:
                                bib_warning('Warning 006: for the entry ending on line #' + unicode(self.i) + \
                                    ' of file "' + self.filename + '", cannot find the abbreviation key "' +
                                    abbrevkey + '". Skipping ...', self.disable)
                                resultstr = self.options['undefstr']
                        fieldstr = ''
                        end_of_field = True
                    else:
                        (fieldstr, resultstr, end_of_field) = self.replace_abbrevs_with_full(fieldstr, resultstr)

                    ## Since we found the comma at the end of this field's contents, we break here to return to the loop
                    ## over fields.
                    if end_of_field:
                        entrystr = fieldstr.strip()
                        break

            ## Strip off any unnecessary white space and remove any newlines.
            resultstr = resultstr.strip().replace('\n',' ')

            ## Having braces around quotes can cause problems when parsing nested quotes, and do not provide any
            ## additional functionality.
            if ('{"}') in resultstr:
                resultstr = resultstr.replace('{"}', '"')
            if ("{'}") in resultstr:
                resultstr = resultstr.replace("{'}", "'")
            if ('{`}') in resultstr:
                resultstr = resultstr.replace('{`}', '`')

            fd[fieldkey] = resultstr

            ## If the field defines a cross-reference, then add it to the "searchkeys", so that when we are culling the
            ## database for faster parsing, we do not ignore the cross-referenced entries.
            if (fieldkey == 'crossref'):
                self.searchkeys.append(resultstr)

        return(fd)

    ## =============================
    def parse_auxfile(self, filename, recursive_call=False, debug=False):
        '''
        Read in an `.aux` file and convert the `\citation{}` entries found there into a dictionary of citekeys and
        citation order number.

        Parameters
        ----------
        filename : str
            The filename of the `.aux` file to parse.
        recursive_call : bool
            Whether this function was called recursively (recursive_call=True), or if it is the top-level call \
            (recursive_call=False). Only in the latter case do we take the keylist and make self.citedict with it.
        '''

        if debug: print('Reading AUX file "' + filename + '" ...')

        ## Check if this file has been called before --- don't allow infinite recursion!
        if filename in self.auxfile_list:
            return

        ## Need to use the "codecs" module to handle UTF8 encoding/decoding properly. Using mode='rU' with the common
        ## "open()" file function doesn't do this probperly, though I don't know why.
        self.filename = filename
        filehandle = codecs.open(os.path.normpath(filename), 'r', 'utf-8')
        self.auxfile_list.append(filename)

        ## First go through the file and grab the list of citation keys. Once we get them all, then we can go through
        ## the list and figure out the numbering.
        for line in filehandle:
            line = line.strip()

            ## If the line begins with "\@input{" then it says to go into a file and look for citations there.
            if line.startswith(r'\@input{'):
                input_filename = line[8:-1].strip()
                self.parse_auxfile(input_filename, recursive_call=True)

            if not line.startswith(r'\citation{'): continue

            ## Remove the "\citation{" from the front and the "}" from the back. If multiple citations are given,
            ## then split them using the comma.
            items = line[10:-1].split(',')
            for item in items:
                self.keylist.append(item)
        filehandle.close()

        if recursive_call:
            return

        ## If you didn't find any citations in the file, issue a warning. Otherwise, build a dictionary of keys giving
        ## the citation keys with values equal to the citation order number. For citation order number, we can't just
        ## start at 1 here, since some citations may occur in a recursive call to this function. Rather, we
        ## need to look into the citation dictionary, grab the highest citation number available there, and increment.
        if not self.keylist:
            bib_warning('Warning 007: no citations found in AUX file "' + filename + '"', self.disable)
        else:
            if not self.citedict:
                q = 1                   ## citation order counter
            else:
                q = max(self.citedict.values())

            self.citedict[self.keylist[0]] = q
            for key in self.keylist[1:]:
                if key in self.citedict: continue
                q += 1
                self.citedict[key] = q

        if debug:
            ## When displaying the dictionary, show it in order-sorted form. Remember to use the user's locale for the
            ## sort.
            for key in sorted(self.citedict, key=self.citedict.get, cmp=locale.strcoll):
                print(key + ': ' + unicode(self.citedict[key]))

        return

    ## =============================
    def parse_bstfile(self, filename):
        '''
        Convert a Bibulous-type bibliography style template into a dictionary.

        The resulting dictionary consists of keys which are the various entrytypes, and values which are the template
        strings. In addition, any formatting options are stored in the "options" key as a dictionary of
        option_name:option_value pairs.

        Parameters
        ----------
        filename : str
            The filename of the Bibulous style template to use.
        '''

        self.filename = filename
        filehandle = codecs.open(os.path.normpath(filename), 'r', 'utf-8')

        ## For the "definition_pattern", rather than matching the initial string up to the first whitespace character,
        ## we match a whitespace-equals-whitespace
        definition_pattern = re.compile(r'\s=\s', re.UNICODE)
        section = 'TEMPLATES'
        continuation = False        ## whether the current line is a continuation of the previous
        abort_script = False        ## if an unsafe object is being used, abort the user_script eval

        for i,line in enumerate(filehandle):
            ## Ignore any comment lines, and remove any comments from data lines.
            if line.startswith('#'): continue
            if ('#' in line):
                idx = line.index('#')
                line = line[:idx]
                if not line.strip(): continue       ## if the line contained only a comment

            if ('EXECUTE {' in line) or ('EXECUTE{' in line) or ('FUNCTION {' in line):
                raise ImportError('The style template file "' + filename + '" appears to be BibTeX format, not '
                                  'Bibulous. Aborting...')

            if line.strip().startswith('TEMPLATES:'):
                section = 'TEMPLATES'
                continuation = False
                continue
            elif line.strip().startswith('SPECIAL-TEMPLATES:'):
                section = 'SPECIAL-TEMPLATES'
                continuation = False
                continue
            elif line.strip().startswith('OPTIONS:'):
                section = 'OPTIONS'
                continuation = False
                continue
            elif line.strip().startswith('DEFINITIONS:'):
                section = 'DEFINITIONS'
                continuation = False
                continue
            elif line.strip().startswith('VARIABLES:'):
                section = 'VARIABLES'
                continuation = False
                continue

            if (section == 'DEFINITIONS'):
                if ('__' in line):
                    bib_warning('Warning 026a: Python script line #' + str(i) + ' of file "' + filename + '" contains'\
                         ' an invalid use of "__".\nAborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'\sos.\S', line, re.UNICODE):
                    bib_warning('Warning 026b: Python script line #' + str(i) + ' of file "' + filename + '" contains'\
                         ' an invalid call to the "os" module.\nAborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'\ssys.\S', line, re.UNICODE):
                    bib_warning('Warning 026c: Python script line #' + str(i) + ' of file "' + filename + '" contains'\
                         ' an invalid call to the "sys" module.\nAborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'\scodecs.\S', line, re.UNICODE):
                    bib_warning('Warning 026c: Python script line #' + str(i) + ' of file "' + filename + '" contains'\
                         ' an invalid call to the "codecs" module.\nAborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'^import\s', line, re.UNICODE):
                    bib_warning('Warning 026d: Python script line #' + str(i) + ' of file "' + filename + '" contains'\
                         ' an invalid call to "import".\nAborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'^import\s', line, re.UNICODE):
                    bib_warning('Warning 026e: Python script line #' + str(i) + ' of file "' + filename + '" contains'\
                         ' an invalid call to the "open()" function.\nAborting script evaluation ...', self.disable)
                    abort_script = True

                self.user_script += line
                if self.debug: print('Adding a line to the BST scripting string: ' + line, end='')

            line = line.strip()

            if (section == 'VARIABLES'):
                if not line: continue
                matchobj = re.search(definition_pattern, line)
                if (matchobj == None):
                    bib_warning('Warning 008a: line #' + str(i) + ' of file "' + filename + '" does not contain' + \
                         ' a valid variable definition.\n Skipping ...', self.disable)
                    continue
                (start,end) = matchobj.span()
                var = line[:start].strip()
                value = line[end:].strip()
                self.user_variables[var] = filter_script(value)
                if self.debug:
                    print('Adding user variable "' + var + '" with value "' + value + '" ...')
            elif (section in ('TEMPLATES','OPTIONS','SPECIAL-TEMPLATES')):
                ## Skip empty lines. It is tempting to put this line above here, but resist the temptation -- putting
                ## it higher above would remove empty lines from the Python scripts in the DEFINITIONS section, which
                ## would make troubleshooting those more difficult.
                if not line: continue
                if not continuation:
                    ## If the line ends with an ellipsis, then remove the ellipsis and set continuation to True.
                    if line.endswith('...'):
                        line = line[:-3].strip()
                        continuation = True

                    matchobj = re.search(definition_pattern, line)
                    if (matchobj == None):
                        bib_warning('Warning 008b: line #' + str(i) + ' of file "' + filename + '" does not contain' +\
                             ' a valid variable definition.\n Skipping ...', self.disable)
                        continue

                    (start,end) = matchobj.span()
                    var = line[:start].strip()
                    value = line[end:].strip()
                else:
                    ## If the line ends with an ellpsis, then remove the ellipsis and set continuation to True.
                    if line.endswith('...'):
                        line = line[:-3].strip()
                        continuation = True
                    else:
                        continuation = False

                    value += line.strip()

                if (section == 'TEMPLATES'):
                    ## The line defines an entrytype template. Check whether this definition is overwriting an already
                    ## existing definition.
                    if (var in self.bstdict) and (self.bstdict[var] != value):
                        bib_warning('Warning 009a: overwriting the existing template variable "' + var + \
                             '" from [' + self.bstdict[var] + '] to [' + value + '] ...', self.disable)
                    self.bstdict[var] = value

                    ## Find out if the template has nested option blocks. If so, then add it to
                    ## the list of nested templates.
                    levels = get_delim_levels(value, ('[',']'))
                    if (2 in levels) and (var not in self.nested_templates):
                        self.nested_templates.append(var)

                    ## Find out if the template contains an implicit loop (an ellipsis not at the end of a line). If
                    ## so then add it to the list of looped templates.
                    if ('...' in value.strip()[:-3]) and (var not in self.looped_templates):
                        loop_data = get_implicit_loop_data(value)
                        self.looped_templates[var] = loop_data

                    if self.debug:
                        print('Setting BST entrytype template "' + var + '" to value "' + value + '"')

                elif (section == 'OPTIONS'):
                    ## The variable defines an option rather than an entrytype. Check whether this definition is
                    ## overwriting an already existing definition.
                    if (var in self.options) and (str(self.options[var]) != value):\
                        bib_warning('Warning 009b: overwriting the existing template option "' + var + '" from [' + \
                             unicode(self.options[var]) + '] to [' + unicode(value) + '] ...', self.disable)
                    ## If the value is numeric or bool, then convert the datatype from string.
                    if self.debug:
                        print('Setting BST option "' + var + '" to value "' + value + '"')

                    if value.isdigit():
                        value = int(value)
                    elif (value in ('True','False')):
                        value = (value == 'True')

                    if (var == 'name_separator') and (value == ''):
                        value = ' '

                    self.options[var] = value

                elif (section == 'SPECIAL-TEMPLATES'):
                    ## The line defines an entrytype template. Check whether this definition is overwriting an already
                    ## existing definition.
                    if (var in self.specials) and (self.specials[var] != value):
                        bib_warning('Warning 009c: overwriting the existing special template variable "' + var + \
                             '" from [' + self.specials[var] + '] to [' + value + '] ...', self.disable)
                    self.specials[var] = value
                    if (var not in self.specials_list):
                        self.specials_list.append(var)

                    if ('.to_namelist()>' in value):
                        self.namelists.append(var)

                    ## Find out if the template has nested option blocks. If so, then add it to
                    ## the list of nested templates.
                    levels = get_delim_levels(value, ('[',']'))
                    if not levels:
                        bib_warning('Warning 036: the style template for entrytype "' + var + '" has unbalanced ' + \
                                    'square brackets. Skipping ...', self.disable)
                        self.specials[var] = ''

                    if (2 in levels) and (var not in self.nested_templates):
                        self.nested_templates.append(var)

                    ## Find out if the template contains an implicit loop (an ellipsis not at the end of a line). If
                    ## so then add it to the list of looped templates.
                    if ('...' in value.strip()[:-3]) and (var not in self.looped_templates):
                        loop_data = get_implicit_loop_data(value)
                        self.looped_templates[var] = loop_data

                    ## Find out if the template contains an implicit index. If so then add it to the list of such.
                    if re.search('\.n\.', value) or re.search('\.n>', value):
                        (varname,_) = var.split('.',1)
                        if (varname not in self.implicitly_indexed_vars):
                            self.implicitly_indexed_vars.append(varname)

                    if self.debug:
                        print('Setting BST special template "' + var + '" to value "' + value + '"')

        filehandle.close()

        if abort_script:
            self.user_script = ''

        ## The "terse_inits" options has to override the "period_after_initial" option.
        if ('terse_inits' in self.options) and  self.options['terse_inits']:
            self.options['period_after_initial'] = False

        ## Next check to see whether any of the template definitions are simply maps to one of the other definitions.
        ## For example, one BST file may have a line of the form
        ##      inbook = incollection
        ## which implies that the template for "inbook" should be mapped to the same template as defined for the
        ## "incollection" entrytype.
        for key in self.bstdict:
            nwords = len(re.findall(r'\w+', self.bstdict[key]))
            if (nwords == 1) and ('<' not in self.bstdict[key]):
                self.bstdict[key] = self.bstdict[self.bstdict[key]]

        ## If the user defined any functions, then we want to evaluate them in a way such that they are available in
        ## other functions.
        if self.user_script and self.options['allow_scripts']:
            if self.debug:
                print('Evaluating the user script:\n' + 'v'*50 + '\n' + self.user_script + '^'*50 + '\n')
            exec(self.user_script, globals())

        ## Next validate all of the template strings to check for formatting errors.
        bad_templates = []
        for key in self.bstdict:
            okay = self.validate_templatestr(self.bstdict[key], key)
            if not okay:
                bad_templates.append(key)

        for bad in bad_templates:
            self.bstdict[bad] = 'Error: malformed template.'

        ## The "special templates" have to be treated differently, since we can't just replace the template with the
        ## "malformed template" message. If the template is not okay, then validate_templatestr() will emit a warning
        ## message. If not okay, then replace the offending template with self.options['undefstr'].
        for key in self.specials:
            okay = self.validate_templatestr(self.specials[key], key)
            if not okay: self.specials[key] = self.options['undefstr']

        if self.debug:
            ## When displaying the BST dictionary, show it in sorted form.
            for key in sorted(self.bstdict, key=self.bstdict.get, cmp=locale.strcoll):
                print('entrytype.' + key + ': ' + unicode(self.bstdict[key]))
            for key in sorted(self.options, key=self.options.get):
                print('options.' + key + ': ' + unicode(self.options[key]))
            for key in sorted(self.specials, key=self.specials.get):
                print('specials.' + key + ': ' + unicode(self.specials[key]))

        return

    ## =============================
    def write_bblfile(self, filename=None, write_preamble=True, write_postamble=True, bibsize=None, debug=False):
        '''
        Given a bibliography database `bibdata`, a dictionary containing the citations called out `citedict`, and a
        bibliography style template `bstdict` write the LaTeX-format file for the formatted bibliography.

        Start with the preamble and then loop over the citations one by one, formatting each entry one at a time, and
        put `\end{thebibliography}` at the end when done.

        Parameters
        ----------
        filename : str, optional
            The filename of the ".bbl" file to write. (Default is to take the AUX file and change its extension to \
            ".bbl".)
        write_preamble : bool, optional
            Whether to write the preamble. (Setting this to False can be useful when writing the bibliography in \
            separate steps, as in the testing suite.)
        write_postamble : bool, optional
            Whether to write the postamble. (Setting this to False can be useful when writing the bibliography in \
            separate steps, as in the testing suite.)
        bibsize : str, optional
            A string the length of which is used to determine the label margin for the bibliography.
        '''

        if (filename == None):
            filename = self.filedict['bbl']
        if not self.citedict:
            print('Warning 034: No citations were found.')
            return
        if not self.bstdict:
            raise ImportError('No template file was found. Aborting writing the BBL file ...')

        if not write_preamble:
            filehandle = open(filename, 'a')
        else:
            filehandle = open(filename, 'w')

        if write_preamble:
            if not bibsize: bibsize = repr(len(self.citedict))
            filehandle.write('\\begin{thebibliography}{' + bibsize + '}\n'.encode('utf-8'))
            filehandle.write("\\providecommand{\\enquote}[1]{``#1''}\n".encode('utf-8'))
            filehandle.write('\\providecommand{\\url}[1]{{\\tt #1}}\n'.encode('utf-8'))
            filehandle.write('\\providecommand{\\href}[2]{#2}\n'.encode('utf-8'))
            if (self.options['bibitemsep'] != None):
                s = '\\setlength{\\itemsep}{' + self.options['bibitemsep'] + '}\n'
                filehandle.write(s.encode('utf-8'))

            if ('preamble' in self.bibdata):
                filehandle.write(self.bibdata['preamble'].encode('utf-8'))

            filehandle.write('\n\n'.encode('utf-8'))

        ## Use a try-except block here, so that if any exception is raised then we can make sure to produce a valid
        ## BBL file.
        try:
            ## First insert special variables, so that the citation sorter and everything else can use them. Also
            ## insert cross-reference data. Doing these here means that we don't have to add lots of extra checks
            ## later.
            for c in self.citedict:
                ## If the citation key is not in the database, then create a fake entry with it, using entrytype
                ## "errormsg", and an item "errormsg" that contains the thing we want printed out in the citation
                ## list to warn the user.
                if c not in self.bibdata:
                    msg = 'citation key ``' + c + '\'\' is not in the bibliography database'
                    bib_warning('Warning 010a: ' + msg, self.disable)
                    errormsg = r'\textit{Warning: ' + msg + '}.'
                    self.bibdata[c] = {'errormsg':errormsg, 'entrytype':'errormsg', 'entrykey':c}

                self.insert_crossref_data(c)
                self.insert_specials(c)

            ## Define a list which contains the citation keys, sorted in the order in which we need for writing into
            ## the BBL file.
            self.create_citation_list()

            if ('<citealnum' in self.specials['citelabel']):
                alphanums = create_alphanum_citelabels(c, self.bibdata, self.citelist)
                for c in self.citelist:
                    res = self.specials['citelabel'].replace('<citealnum>',alphanums[c])
                    self.bibdata[c]['citelabel'] = res

            ## Write out each individual bibliography entry. Some formatting options will actually cause the entry to
            ## be deleted, so we need the check below to see if the return string is empty before writing it to the
            ## file.
            for c in self.citelist:
                ## Verbose output is for debugging.
                if debug: print('Writing entry "' + c + '" to "' + filename + '" ...')

                ## Now that we have generated all of the "special" fields, we can call the bibitem formatter to
                ## generate the output for this entry.
                s = self.format_bibitem(c)
                if (s != ''):
                    ## Need two line EOL's here and not one so that backrefs can work properly.
                    filehandle.write((s + '\n').encode('utf-8'))
        except Exception, err:
            ## Swallow the exception
            print('Exception encountered: ' + repr(err))
        finally:
            if write_postamble:
                filehandle.write('\n\\end{thebibliography}\n'.encode('utf-8'))
            filehandle.close()

        return

    ## ===================================
    def create_citation_list(self):
        '''
        Create the list of citation keys, sorted into the proper order.
        '''

        self.citelist = []
        self.sortlist = []

        ## If the sortkeys all begin with numbers, then sort numerically (i.e. -100 before -99, 99 before 100, etc).
        humansort = True

        ## Generate a sortkey for each citation.
        for c in self.citedict:
            s = self.bibdata[c]['sortkey']
            self.sortlist.append(s)
            self.citelist.append(c)

            if not re.search(r'^-?[0-9]+', s, re.UNICODE) and not s.startswith(self.options['undefstr']):
                humansort = False

        ## This part can be a little tricky. If the sortkey is generated such that it begins with an integer, then we
        ## should make sure that negative-values get sorted in front of positive ones. This happens correctly in simple
        ## sort() but not when we use locale's "strcoll". So we have to separate the two cases manually. Also, use
        ## [::-1] on the negative integers because they need to be ordered from largest number to smallest.
        if humansort:
            neg_idx = [i for (i,k) in enumerate(self.sortlist) if k[0] == '-']
            pos_idx = [i for (i,k) in enumerate(self.sortlist) if k[0] != '-']
            pos_sortkeys = [self.sortlist[x] for x in pos_idx]
            neg_sortkeys = [self.sortlist[x] for x in neg_idx]
            pos_citekeys = [self.citelist[x] for x in pos_idx]
            neg_citekeys = [self.citelist[x] for x in neg_idx]

            pos_idx = argsort(pos_sortkeys)
            neg_idx = argsort(neg_sortkeys, reverse=True)
            self.sortlist = [neg_sortkeys[x] for x in neg_idx] + [pos_sortkeys[x] for x in pos_idx]
            self.citelist = [neg_citekeys[x] for x in neg_idx] + [pos_citekeys[x] for x in pos_idx]
        else:
            idx = argsort(self.sortlist)
            self.sortlist = [self.sortlist[x] for x in idx]
            self.citelist = [self.citelist[x] for x in idx]

        ## If using a citation order which is descending rather than ascending, then reverse the list.
        if (self.options['sort_order'].lower() == 'reverse'):
            self.sortlist = self.sortlist[::-1]
            self.citelist = self.citelist[::-1]

        ## Finally, generate the "sortnum" for the reference --- the order in which it will appear in the reference
        ## list. This is different from "citenum", which is the order of citation in the text. For example, if
        ## the reference list is sorted alphabetically, but you want the list enumerated, then you need "sortnum"
        ## to get the enumerated value for each reference.
        for i,c in enumerate(self.citelist):
            self.bibdata[c]['sortnum'] = i+1

            ## If "sortnum" appears somewhere inside the special template definitions, where it is not yet defined,
            ## then we need to go back and redo the specials.
            foundit = False
            for key in self.specials.keys():
                if ('sortnum' in self.specials[key]):
                    foundit = True
                    break

            if foundit:
                self.insert_specials(c)

        if self.debug:
            for i in range(len(self.citelist)):
                print('citekey=%25s: sortkey=%s' % (self.citelist[i], self.sortlist[i]))

        return

    ## =============================
    def format_bibitem(self, citekey, debug=False):
        '''
        Create the "\bibitem{...}" string to insert into the ".bbl" file.

        This is the workhorse function of Bibulous. For a given citation key, find the resulting entry in the
        bibliography database. From the entry's `entrytype`, lookup the relevant template in bstdict and start
        replacing template variables with formatted elements of the database entry. Once you've replaced all template
        variables, you're done formatting that entry. Write the result to the BBL file.

        Parameters
        ----------
        citekey : str
            The citation key.

        Returns
        -------
        itemstr : str
            The string containing the \bibitem{} citation key and LaTeX-formatted string for the formatted \
            bibliography. (That is, this string is designed to be inserted directly into the LaTeX document.)
        '''

        c = citekey
        if (c == 'preamble'):
            return('')

        entry = self.bibdata[c]
        entrytype = entry['entrytype']

        ## If the journal format uses ProcSPIE like a journal, then you need to change the entrytype from
        ## "inproceedings" to "article", and add a "journal" field.
        if self.options['procspie_as_journal'] and (entrytype == 'inproceedings') and \
            ('series' in entry) and (entry['series'] in ['Proc. SPIE','procspie']):
            entrytype = 'article'
            entry['entrytype'] = 'article'
            entry['journal'] = 'Proc.\\ SPIE'

        if (entrytype in self.bstdict):
            templatestr = self.bstdict[entrytype]
        elif (entrytype == 'errormsg'):
            if (unicode(self.bibdata[c]['citelabel']) == 'None'):
                itemstr = r'\bibitem{' + c + '}\n' + self.bibdata[c]['errormsg']
            else:
                itemstr = r'\bibitem[' + self.bibdata[c]['citelabel'] + ']{' + c + '}\n' + self.bibdata[c]['errormsg']
            return(itemstr)
        else:
            msg = 'entrytype "' + entrytype + '" does not have a template defined in the .bst file'
            bib_warning('Warning 011: ' + msg + '. Skipping ...', self.disable)
            return('')

        ## Before checking which variables are defined and which not, we first need to evaluate the user-defined
        ## variables or else they will always be "undefined". To make this work, we also need to provide the user
        ## shortcut names:
        if self.user_variables and self.options['allow_scripts']:
            options = self.options      # pyflakes:ignore
            assert options
            citedict = self.citedict    # pyflakes:ignore
            bstdict = self.bstdict      # pyflakes:ignore
            bibdata = self.bibdata      # pyflakes:ignore
            for user_var_name in self.user_variables:
                user_var_value = eval(self.user_variables[user_var_name])
                entry[user_var_name] = user_var_value

        bibitem_label = self.bibdata[c]['citelabel']

        if (unicode(bibitem_label) == 'None'):
            itemstr = r'\bibitem{' + c + '}\n'
        else:
            itemstr = r'\bibitem[' + bibitem_label + ']{' + c + '}\n'

        if debug:
            print('Formatting entry "' + citekey + '"')
            print('Template: "' + self.bstdict[entrytype] + '"')
            print('Field data: ' + repr(entry))

        try:
            ## Substitute the template variables with fields from the bibliography entry.
            templatestr = self.template_substitution(templatestr, citekey)
            ## Add the filled-in template string onto the "\bibitem{...}\n" line in front of it.
            itemstr = itemstr + templatestr
        except SyntaxError, err:
            itemstr = itemstr + '\\textit{' + err + '}.'
            bib_warning('Warning 013: ' + err, self.disable)

        ## If there are nested operators on the string, replace all even-level operators with \{}. Is there any need to
        ## do this with \textbf{} and \texttt{} as well?
        if (itemstr.count('\\textit{') > 1):
            itemstr = enwrap_nested_string(itemstr, delims=('{','}'), odd_operator=r'\textit', \
                                           even_operator=r'\textup')
        if (itemstr.count('\\textbf{') > 1):
            itemstr = enwrap_nested_string(itemstr, delims=('{','}'), odd_operator=r'\textbf', \
                                           even_operator=r'\textmd')

        if self.options['wrap_nested_quotes']:
            ## If there are any nested quotation marks in the string, then we need to modify the formatting properly.
            ## If there are any apostrophes or foreign words that use apostrophes in the string then the current code
            ## will raise an exception.
            itemstr = enwrap_nested_quotes(itemstr, disable=self.disable)

        return(itemstr)

    ## =============================
    def insert_crossref_data(self, entrykey, fieldname=None):
        '''
        Insert crossref info into a bibliography database dictionary.

        Loop through a bibliography database dictionary and, for each entry which has a "crossref" field, locate the
        crossref entry and insert any missing bibliographic information into the main entry's fields.

        Parameters
        ----------
        entrykey : str
            The key of the bibliography entry to query.
        fieldname : str, optional
            The name of the field to check. If fieldname==None, then check all fields.

        Returns
        -------
        foundit : bool
            Whether the function found a crossref for the queried field. If multiple fieldnames were input, then \
            `foundit` will be True if a crossref is located for any one of them.
        '''

        ## First check that the entrykey exists.
        if ('errormsg' in self.bibdata[entrykey]):
            return
        if ('crossref' not in self.bibdata[entrykey]):
            return

        bibentry = self.bibdata[entrykey]

        if (fieldname == None):
            fieldnames = bibentry.keys()
        else:
            if isinstance(fieldname, list):
                fieldnames = fieldname
            else:
                fieldnames = [fieldname]

        ## Check that the cross-referenced entry actually exists. If not, then just move on.
        if (self.bibdata[entrykey]['crossref'] in self.bibdata):
            crossref_keys = self.bibdata[self.bibdata[entrykey]['crossref']]
        else:
            bib_warning('Warning 015: bad cross reference. Entry "' + entrykey + '" refers to ' + 'entry "' + \
                 self.bibdata[entrykey]['crossref'] + '", which doesn\'t exist.', self.disable)
            return

        for k in crossref_keys:
            if (k in bibentry): continue
            if (k not in fieldnames):
                self.bibdata[entrykey][k] = self.bibdata[self.bibdata[entrykey]['crossref']][k]

        ## What a "booktitle" is in the entry is normally a "title" in the crossref.
        if ('title' in crossref_keys) and ('booktitle' not in self.bibdata[entrykey]):
            self.bibdata[entrykey]['booktitle'] = self.bibdata[self.bibdata[entrykey]['crossref']]['title']

        return

    ## =============================
    def write_citeextract(self, outputfile, write_abbrevs=False):
        '''
        Extract a sub-database from a large bibliography database, with the former containing only those entries cited
        in the .aux file (and any relevant cross-references).

        Parameters
        ----------
        filedict :  str
            The dictionary filenames must have keys "aux",  "bst", and "bib".
        outputfile : str, optional
            The filename to use for writing the extracted BIB file.
        write_abbrevs : bool
            Whether or not to write the abbreviations to the BIB file. Since the abbreviations are already inserted \
            into the database entries, they are no longer needed, but may be useful for future editing and adding of \
            entries to the database file.
        '''

        ## The "citedict" contains only those items directly cited, but we also need any cross-referenced items as
        ## well, so let's add those.
        crossref_list = []
        for key in self.citedict:
            if key not in self.bibdata: continue
            if ('crossref' in self.bibdata[key]) and (self.bibdata[key]['crossref'] in self.bibdata):
                crossref_list.append(self.bibdata[key]['crossref'])

        citekeylist = self.citedict.keys()
        if crossref_list: citekeylist.extend(crossref_list)

        ## A dict comprehension to extract only the relevant items in "bibdata". Note that these entries are mapped by
        ## reference and not by value --- any changes to "bibextract" will also be reflected in "self.bibdata" is the
        ## change is to a mutable entry (such as a list or a dict).
        bibextract = {c:self.bibdata[c] for c in citekeylist if c in self.bibdata}
        abbrevs = self.abbrevs if write_abbrevs else None
        export_bibfile(bibextract, outputfile, abbrevs)
        return

    ## =============================
    def write_authorextract(self, searchname, outputfile=None, write_abbrevs=False):
        '''
        Extract a sub-database from a large bibliography database, with the former containing only those entries citing
        the given author/editor.

        Parameters
        ----------
        searchname : str or dict
            The string or dictionary for the author's name. This can be, for example, "Bugs E. Bunny" or \
            {'first':'Bugs', 'last':'Bunny', 'middle':'E'}.
        outputfile : str, optional
            The filename of the extracted BIB file to write.
        write_abbrevs : bool
            Whether or not to write the abbreviations to the BIB file. Since the abbreviations are already inserted \
            into the database entries, they are no longer needed, but may be useful for future editing and adding of \
            entries to the database file.
        '''

        if not isinstance(searchname, basestring):
            raise TypeError('The input search name ["' + unicode(searchname) + '"] is not a valid string.')
        if not outputfile:
            outputfile = self.filedict['aux'][:-4] + '_authorextract.bib'

        searchname = namestr_to_namedict(searchname, self.disable)
        nkeys = len(searchname.keys())
        sep = self.options['name_separator']

        ## Find out if any of the tokens in the search name are initials. If so, then we need to perform the search
        ## over initialized names and not full names. Save the set of booleans (one for each name part) in a dictionary
        ## to use in the search loop below.
        name_is_initialized = {}
        for key in searchname:
            name_is_initialized[key] = searchname[key].endswith('.')

        ## This is the dictionary we will stuff extracted entries into.
        bibextract = {}
        nentries = 0        ## count the number of entries found

        for k in self.bibdata:
            ## Get the list of name dictionaries from the entry.
            name_list_of_dicts = []
            if ('author' in self.bibdata[k]):
                name_list_of_dicts = namefield_to_namelist(self.bibdata[k]['author'], key=k, sep=sep, disable=self.disable)
            if ('editor' in self.bibdata[k]):
                namelist = namefield_to_namelist(self.bibdata[k]['editor'], key=k, sep=sep, disable=self.disable)
                if not ('author' in self.bibdata[k]):
                    name_list_of_dicts = namelist
                else:
                    ## If the entry has both authors and editors, then just merge the two name lists.
                    name_list_of_dicts += namelist

            if not name_list_of_dicts:
                continue

            ## Compare each name dictionary in the entry with the input author's name dict. All of an author's name
            ## keys must equal an entry's name key to produce a match.
            for name in name_list_of_dicts:
                if (searchname['last'] not in name['last']): continue

                key_matches = 0
                for namekey in searchname:
                    if (namekey in name):
                        if name_is_initialized[namekey]:
                            thisname = initialize_name(name[namekey], options={'period_after_initial':True}) + '.'
                        else:
                            thisname = name[namekey]

                        if (thisname == searchname[namekey]):
                            key_matches += 1
                            if self.debug:
                                print('Found match in entry "%s": name[%s] = %s from "%s"' % \
                                      (k, namekey, name[namekey], repr(name)))

                if (key_matches == nkeys):
                    bibextract[k] = self.bibdata[k]
                    del bibextract[k]['entrykey']
                    nentries += 1
                    if self.debug: print('Match FULL NAME in entry "' + k + '": ' + repr(name))

        abbrevs = self.abbrevs if write_abbrevs else None
        export_bibfile(bibextract, outputfile, abbrevs)

        return

    ## =============================
    def replace_abbrevs_with_full(self, fieldstr, resultstr):
        '''
        Given an input str, locate the abbreviation key within it and replace the abbreviation with its full form.

        Once the abbreviation key is found, remove it from the "fieldstr" and add the full form to the "resultstr".

        Parameters
        ==========
        fieldstr : str
            The string to search for the abbrevation key.
        resultstr : str
            The thing to hold the abbreviation's full form. (Note that it might not be empty on input.)

        Returns
        =======
        fieldstr : str
            The string to search for the abbrevation key.
        resultstr : str
            The thing to hold the abbreviation's full form.
        end_of_field : bool
            Whether the abbreviation key was at the end of the current field.
        '''

        end_of_field = False

        ## The "abbrevkey_pattern" seaerches for the first '#' or ',' that is not preceded by a backslash. If this
        ## pattern is found, then we've found the *end* of the abbreviation key.
        for match in re.finditer(self.abbrevkey_pattern, fieldstr):
            endpos = match.end()
            if (match.group(0)[0] == '#'):
                abbrevkey = fieldstr[:endpos-1].strip()
                ## If the "abbreviation" is an integer, then it's not an abbreviation but rather a number, and just
                ## return it as-is.
                if abbrevkey.isdigit() or not self.options['use_abbrevs']:
                    resultstr += unicode(abbrevkey)
                elif (abbrevkey not in self.abbrevs):
                    bib_warning('Warning 016a: for the entry ending on line #' + unicode(self.i) + ' of file "' + \
                         self.filename + '", cannot find the abbreviation key "' + abbrevkey + '". Skipping ...',
                         self.disable)
                    resultstr += self.options['undefstr']
                else:
                    resultstr += self.abbrevs[abbrevkey].strip()
                fieldstr = fieldstr[endpos+1:].strip()
                break
            elif (match.group(0)[0] == ','):
                abbrevkey = fieldstr[:endpos-1].strip()
                ## If the "abbreviation" is an integer, then it's not an abbreviation
                ## but rather a number, and just return it as-is.
                if abbrevkey.isdigit() or not self.options['use_abbrevs']:
                    resultstr += unicode(abbrevkey)
                elif (abbrevkey not in self.abbrevs):
                    bib_warning('Warning 016b: for the entry ending on line #' + unicode(self.i) + ' of file "' + \
                         self.filename + '", cannot find the abbreviation key "' + abbrevkey + '". Skipping ...',
                         self.disable)
                    resultstr += self.options['undefstr']
                else:
                    resultstr += self.abbrevs[abbrevkey].strip()

                fieldstr = fieldstr[endpos+1:].strip()
                end_of_field = True
                break
            else:
                raise SyntaxError('if-else mismatch inside replace_abbrevs_with_full().')

        return(fieldstr, resultstr, end_of_field)

    ## =============================
    def write_auxfile(self, filename=None):
        '''
        Given the input database file(s) and style file(s), write out an AUX file containing citations to all unique
        database entries.

        This function is only provided as a utility, and is not actually used except during troubleshooting.

        Parameters
        ----------
        filename : str
            The filename of the auxfile to write.
        '''

        if (filename == None):
            filename = self.filedict['aux']

        filehandle = open(filename, 'w')

        for entry in self.bibdata:
            filehandle.write('\\citation{' + entry + '}\n'.encode('utf-8'))

        filehandle.write('\n')
        filehandle.write('\\bibdata{')
        for f in self.filedict['bib']:
            filehandle.write(f)
            if (f != self.filedict['bib'][-1]):
                filehandle.write(',')
        filehandle.write('}\n')
        filehandle.write('\\bibstyle{')
        for f in self.filedict['bst']:
            filehandle.write(f)
            if (f != self.filedict['bst'][-1]):
                filehandle.write(',')
        filehandle.write('}\n')
        filehandle.close()
        return

    ## =============================
    def get_bibfilenames(self, filename):
        '''
        If the input is a filename ending in `.aux`, then read through the `.aux` file and locate the lines
        `\bibdata{...}` and `\bibstyle{...}` to get the filename(s) for the bibliography database and style template.

        Also determine whether to set the `culldata` flag. If the input is a single AUX filename, then the default is
        to set culldata=True. If the input is a list of filenames, then assume that this is the complete list of files
        to use (i.e. ignore the contents of the AUX file except for generating the citedict), and set culldata=False.

        Parameters
        ----------
        filename : str
            The "auxiliary" file, containing citation info, TOC info, etc.

        Returns
        -------
        filedict : dict
            A dictionary with keys `aux`, `bbl`, `bib`, `bst`, `extract`, and `tex`, each entry of which contains a \
            list of filenames.
        '''

        bibfiles = []
        bstfiles = []
        auxfile = ''
        bblfile = ''
        texfile = ''
        extractfile = ''

        bibres = None
        bstres = None

        if isinstance(filename, basestring) and filename.endswith('.aux'):
            auxfile = os.path.normpath(os.path.abspath(filename))
            path = os.path.normpath(os.path.dirname(auxfile))

            s = open(filename, 'rU')
            for line in s.readlines():
                line = line.decode('utf-8').strip()
                if line.startswith('%'): continue
                if line.startswith('\\bibdata{'):
                    line = line[9:]
                    indx = line.index('}')
                    bibres = line[:indx]
                if line.startswith('\\bibstyle{'):
                    line = line[10:]
                    indx = line.index('}')
                    bstres = line[:indx]

            if (bibres == None):
                print('Bibulous cannot find a bibliography database specified in "' + filename + '". '
                                 'Aborting generation of BBL file')
                return

            if (bstres == None):
                print('Bibulous cannot find a bibliography template specified in "' + filename + '". '
                                 'Aborting generation of BBL file')
                return

            ## Now we have the strings from the ".tex" file that describing the bibliography filenames. If these are
            ## lists of filenames, then split them out.
            if (',' in bibres):
                bibres = bibres.split(',')      ## if a list of files, then split up the list pieces
            else:
                bibres = [bibres]

            for r in bibres:
                ## If the filename is missing the extension, then add it.
                if not r.endswith('.bib'):
                    r += '.bib'

                ## If the filename has a relative address, convert it to an absolute one. Linux absolute paths begin
                ## with a forward slash. Windows absolute paths begin with a drive letter and a colon.
                if not r.startswith('/') or (r[0].isalpha() and r[1] == ':'):
                    r = os.path.normpath(os.path.join(path, r))
                elif r.startswith('./'):
                    r = os.path.normpath(os.path.join(path, r[2:]))

                bibfiles.append(r)

            ## Next do the same thing for the ".bst" files.
            if (',' in bstres):
                bstres = bstres.split(',')      ## if a list of files, then split up the list pieces
            else:
                bstres = [bstres]

            for r in bstres:
                ## If the filename is missing the extension, then add it.
                if not r.endswith('.bst'):
                    r += '.bst'

                ## If the filename has a relative address, convert it to an absolute one. Linux absolute paths begin
                ## with a forward slash Windows absolute paths begin with a drive letter and a colon.
                if not r.startswith('/') or (r[0].isalpha() and r[1] == ':'):
                    r = os.path.normpath(os.path.join(path, r))
                elif r.startswith('./'):
                    r = os.path.normpath(os.path.join(path, r[2:]))

                bstfiles.append(r)

            ## Finally, normalize the file strings to work on any platform.
            for i in range(len(bibfiles)):
                bibfiles[i] = os.path.normpath(bibfiles[i])
            for i in range(len(bstfiles)):
                bstfiles[i] = os.path.normpath(bstfiles[i])

        ## Or if the input is only a BIB file, then go off of that.
        elif isinstance(filename, basestring) and filename.endswith('.bib'):
            self.culldata = False
            bibfiles = [os.path.normpath(filename)]

        ## Or of the input is a list, then we can go through all the filenames in the list.
        elif isinstance(filename, (list, tuple)):
            self.culldata = False
            ## All the work above was to locate the filenames from a single AUX file. However, if the input is a list of
            ## filenames, then constructing the filename dictionary is simple.
            for f in filename:
                f = os.path.abspath(f)
                if f.endswith('.aux'): auxfile = os.path.normpath(f)
                elif f.endswith('.bib'): bibfiles.append(os.path.normpath(f))
                elif f.endswith('.bst'): bstfiles.append(os.path.normpath(f))
                elif f.endswith('.bbl'): bblfile = os.path.normpath(f)
                elif f.endswith('.tex'): texfile = os.path.normpath(f)

        if not bblfile:
            bblfile = auxfile[:-4] + '.bbl'
        if not texfile and auxfile:
            texfile = auxfile[:-4] + '.tex'
        if not extractfile:
            extractfile = auxfile[:-4] + '-extract.bib'

        ## Now that we have the filenames, build the dictionary of BibTeX-related files.
        self.filedict['bib'] = bibfiles
        self.filedict['bst'] = bstfiles
        self.filedict['tex'] = texfile
        self.filedict['aux'] = auxfile
        self.filedict['bbl'] = bblfile
        self.filedict['extract'] = extractfile

        if self.debug:
            print('bib files: ' + repr(bibfiles))
            print('bst files: ' + repr(bstfiles))
            print('tex file: "' + unicode(texfile) + '"')
            print('aux file: "' + unicode(auxfile) + '"')
            print('bbl file: "' + unicode(bblfile) + '"')
            print('ext file: "' + unicode(extractfile) + '"')

        return

    ## =============================
    def check_citekeys_in_datakeys(self):
        '''
        Check to see if all of the citation keys (from the AUX file) exist within the current set of database entrykeys.

        Returns
        -------
        is_complete : bool
            True if all citations exist in the database, False otherwise.
        '''

        citekeys = set(self.citedict.keys())
        datakeys = set(self.bibdata.keys())
        diff = citekeys.difference(datakeys)

        if self.debug:
            print('Checking the overlap between citation keys and database keys ...')
            print('The list of keys not found in the current database:')
            print(diff)

        if diff:
            return(False)
        else:
            return(True)

    ## =============================
    def add_crossrefs_to_searchkeys(self):
        '''
        Add any cross-referenced entrykeys into the `searchkeys`, the list which is used to cull the database so that
        only necessary entries are parsed.
        '''

        ## When self.culldata==True, the problem is that if a crossref refers to an entry that was not among the
        ## citation keys, then the database parser will not know to place that entry into the bibdata dictionary. Thus,
        ## if we happen to run across an entry with missing data, and it has a crossref that is not in the database,
        ## then we have to go back and parse the database a second time, this time adding the crossreferenced items.
        ## Once that's done, *then* we can add cross-referenced data into the original cited entries.
        crossref_list = []
        for key in self.bibdata:
            if ('crossref' in self.bibdata[key]):
                crossref_list.append(self.bibdata[key]['crossref'])

        if crossref_list:
            self.searchkeys += crossref_list
        return

    ## =============================
    def insert_specials(self, entrykey):
        '''
        Insert "special" fields into a database entry.

        Parameters
        ----------
        entrykey : str
            The key of the entry to which we want to add special fields.
        '''

        entry = self.bibdata[entrykey]

        if ('pages' in entry):
            (startpage,endpage) = parse_pagerange(entry['pages'], entrykey, self.disable)
            entry['startpage'] = startpage
            entry['endpage'] = endpage

        if ('doi' in entry) and self.options['autocomplete_doi']:
            if not entry['doi'].startswith('http://dx.doi.org/'):
                entry['doi'] = 'http://dx.doi.org/' + entry['doi']

        ## Define the variables "citekey" and "citenum".
        self.bibdata[entrykey]['citekey'] = entrykey
        if self.citedict:
            #ncites = len(self.citedict)
            #ndigits = 1 + int(log10(ncites))    ## note that this requires import of: from math import log10
            citenum = unicode(self.citedict[entrykey])
        else:
            citenum = '1'

        self.bibdata[entrykey]['citenum'] = citenum

        ## Next loop through the "special" variables. These are variable definitions from the SPECIAL-
        ## TEMPLATES section of the style file. Note that rather than looping through
        ## self.specials.keys(), we loop through "self.specials_list" because we want it to be ordered.
        for key in self.specials_list:
            ## Only insert the user-defined special field if the field is missing.
            if (key in entry):
                continue

            templatestr = self.specials[key]

            ## Need to treat citealpha specially. Check if it needs to be present before anything else is defined.
            if ('<citealpha.' in templatestr) or ('<citealpha>' in templatestr):
                citealpha = create_citation_alpha(entry, self.options)
                self.bibdata[entrykey]['citealpha'] = citealpha

            ## If this special template is an implicitly indexed one, then it can only be used after explicit index
            ## replacement (such as within an implicit loop) and not by itself, so we have to skip it here. We
            ## can't use "if (key in self.implicitly_indexed_vars)" here because the "key" contains the implicit
            ## index too (i.e. "name.n" and not "name"), and so the strings in the "implicitly_indexed_vars" list
            ## are not quite what we have in our keys here.
            template_has_implicit_index = True if re.search(self.implicit_index_pattern, templatestr) else False
            if re.search('\.n\.', key) or re.search('\.n$', key) or template_has_implicit_index:
                continue

            ## Substitute other entry fields into the template to generate the formatted result. Note that if the
            ## special template contains an implicit loop, then we DO NOT fill it out here. Filling out an implicit loop
            ## has to be done while performing template substitution because it requires querying entry fields, and is
            ## not a matter of creating entry fields.
            res = self.template_substitution(templatestr, entrykey, templatekey=key)

            ## Insert the result as a new field in the database entry. Note that the "(self.options['undefstr'] not in res)"
            ## piece of code is not quite ideal, but it is an easy solution that has a low probability of breaking
            ## (low prob. that a user will need to use the "undefstr" in a template).
            if template_has_implicit_index and (self.options['undefstr'] not in res):
                self.bibdata[entrykey][key] = res
            elif (res not in (None, '', self.options['undefstr'])):
                self.bibdata[entrykey][key] = res

        return

    ## =============================
    def validate_templatestr(self, templatestr, key):
        '''
        Validate the template string so that it contains no formatting errors.

        Parameters
        ----------
        templatestr : str
            The template string to be validated.
        key : str
            The name of the variable that uses this template.

        Returns
        -------
        okay : bool
            Whether or not the template is properly formatted.
        '''

        okay = True

        ## Make sure that there are the same number of open as closed brackets.
        num_obrackets = templatestr.count('[')
        num_cbrackets = templatestr.count(']')
        if (num_obrackets != num_cbrackets):
            msg = 'In the template for "' + key + '" there are ' + unicode(num_obrackets) + \
                  ' open brackets "[", but ' + unicode(num_cbrackets) + ' close brackets "]" in the formatting string'
            bib_warning('Warning 012: ' + msg, self.disable)
            okay = False

        ## Check that no ']' appears before a '['.
        levels = get_delim_levels(templatestr, ('[',']'))
        if (-1 in levels):
            msg = 'A closed bracket "]" occurs before a corresponding open bracket "[" in the ' + \
                  'template string "' + templatestr + '"'
            bib_warning('Warning 027: ' + msg, self.disable)
            okay = False

        ## Finally, check that no '[', ']', or '|' appear inside a variable name.
        variables = re.findall(r'<.*?>', templatestr)
        for var in variables:
            if ('[' in var):
                msg = 'An invalid "[" character appears inside the template variable "' + var + '"'
                bib_warning('Warning 028a: ' + msg, self.disable)
                okay = False
            if (']' in var):
                msg = 'An invalid "]" character appears inside the template variable "' + var + '"'
                bib_warning('Warning 028b: ' + msg, self.disable)
                okay = False
            if ('|' in var):
                msg = 'An invalid "|" character appears inside the template variable "' + var + '"'
                bib_warning('Warning 028c: ' + msg, self.disable)
                okay = False
            if ('<' in var[1:-1]):
                msg = 'An invalid "<" character appears inside the template variable "' + var + '"'
                bib_warning('Warning 028d: ' + msg, self.disable)
                okay = False

        return(okay)

    ## ===================================
    def fillout_implicit_indices(self, templatestr, entrykey, templatekey=None):
        '''
        From a template containing an implicit loop ('...' notation), build a full-size template without an ellipsis.

        Right now, the code only allows one implicit loop in any given template.

        Parameters
        ----------
        templatestr : str
            The input template string (containing the implicit loop ellipsis notation).
        entrykey : str
            The key of the bibliography entry to query.
        templatekey : str
            If this template is for a special variable rather than an entrytype, then this key will tell which \
            special variable is being operated on.

        Returns
        -------
        new_templatestr : str
            The new template with the ellipsis replaced with the loop-generated template variables and "glue".
        '''

        ## To look for an indexed variable, it has to have the form of a (dot plus an integer), or (dot plus 'n'), or
        ## (dot plus 'N'); and then followed by either another dot or by '>'.
        has_index = True if re.search(self.index_pattern, templatestr) else False
        has_implicit_loop = ('...' in templatestr)

        if not has_implicit_loop and not has_index:
            return(templatestr)
        elif has_index and not has_implicit_loop:
            ## Get a list of the indexed variables.
            indexed_vars = self.get_indexed_vars_in_template(templatestr)

            for v in indexed_vars:
                elem = get_variable_name_elements(v)
                varname = elem['name'] + '.' + elem['prefix'] + 'n'
                if (varname in self.specials):
                    ## Replace ".n" with "." plus an explicit index.
                    templatestr = templatestr.replace('<'+v+'>', self.specials[varname])
                    templatestr = re.sub(r'(?<=\.)n(?=\.)|(?<=\.)n(?=>)', elem['index'], templatestr)
            return(templatestr)

        names = get_names(self.bibdata[entrykey], templatestr)
        if not names:
            return(templatestr)
        num_names = len(names)

        ## Get the key for the template to look up in the looped template data dictionary (generated when the BST
        ## file is parsed).
        if (templatekey is None):
            templatekey = self.bibdata[entrykey]['entrytype']

        loop_data = self.looped_templates[templatekey]
        loop_varname = loop_data['varname']
        loop_start_index = loop_data['start_index']
        regular_glue = loop_data['glue']
        loop_lhs_prefix = loop_data['var_prefix']
        loop_lhs_suffix = loop_data['var_suffix']
        loop_end_index = loop_data['end_index']
        last_glue = loop_data['last_glue']
        last_glue_if_only_two = loop_data['last_glue_if_only_two']
        before_loop_stuff = loop_data['before_loop_stuff']
        after_loop_stuff = loop_data['after_loop_stuff']

        #print('templatestr=', templatestr)
        #print('self.looped_templates:', self.looped_templates.keys())
        #pdb.set_trace()

        ## Check that the indices are valid.
        if loop_start_index.isdigit():
            loop_start_index = int(loop_start_index)
        elif (loop_start_index == 'N'):
            loop_start_index = num_names - 1
        else:
            msg = 'Warning 031a: the template string "' + templatestr + '" is malformed. The index element "' + \
                  loop_start_index + '" is not recognized.'
            bib_warning(msg)

        ## Check that the indices are valid.
        if not loop_end_index.isdigit() and (loop_end_index != 'N'):
            msg = 'Warning 031b: the template string "' + templatestr + '" is malformed. The index element "' + \
                  loop_end_index + '" is not recognized.'
            bib_warning(msg)

        ## What is the maximum number of allowed names? If the number of names in the namelist is more than the maximum
        ## allowed, then we need to replace the end of the formatted namelist with the "etal_message". Note that, in
        ## BibTeX-formatted name fields, if the last name is simply "others", then it signals that the list is
        ## incomplete, and we should add an "et al." message.
        if (names[-1]['last'].lower() == 'others'):
            maxnames = num_names - 1
        elif (loop_end_index == 'N'):
            maxnames = num_names
        else:
            maxnames = int(loop_end_index) + 1

        too_many_names = (num_names > maxnames)
        loop_end_index = min((num_names,maxnames+1)) - 1
        if (loop_end_index == 0): loop_end_index = 1

        ## If there are only two items in the list to loop over, then use "last_glue_if_only_two", else use "last_glue".
        if (num_names == 2):
            rhs_glue = last_glue_if_only_two
        else:
            rhs_glue = last_glue

        ## Create the implicit loop, applying "glue" between each template variable that you generate. Here we take the
        ## part of the variable name to the left of the index and the part to the right of the index, and put them
        ## back together while replacing the index "n" with the number determined by the loop index.
        new_templatestr = ''
        for n in range(loop_start_index, loop_end_index):
            name_part = loop_varname + '.' + str(n)

            ## Next find if the variable name itself has a template.
            if (name_part in self.specials):
                name_part = self.specials[name_part]
            elif (loop_varname in self.implicitly_indexed_vars):
                name_part = self.specials[loop_varname + '.n']
                name_part = re.sub(r'\.n\.', '.'+str(n)+'.', name_part)
                name_part = re.sub(r'\.n>', '.'+str(n)+'>', name_part)

            new_templatestr += name_part + loop_lhs_suffix
            if (n < loop_end_index-1):
               new_templatestr += regular_glue

        ## Now do the same thing for the endpoint variable of the implicit loop. The endpoint is handled outside of the
        ## loop itself because the "glue" element is often different between the penultimate and the ultimate names.
        if too_many_names:
            new_templatestr += self.options['etal_message']
        elif (num_names > 1):
            n += 1
            name_part = loop_varname + '.' + str(n)
            if (name_part in self.specials):
                name_part = self.specials[name_part]
                new_templatestr += rhs_glue + name_part + loop_lhs_suffix
            elif (loop_varname in self.implicitly_indexed_vars):
                name_part = self.specials[loop_varname + '.n']
                name_part = re.sub(r'\.n\.', '.'+str(n)+'.', name_part)
                name_part = re.sub(r'\.n>', '.'+str(n)+'>', name_part)
                new_templatestr += rhs_glue + name_part + loop_lhs_suffix
            else:
                new_templatestr += rhs

        new_templatestr = before_loop_stuff + new_templatestr + after_loop_stuff

        #print('templatestr=', templatestr)
        #print('new_templatestr=', new_templatestr)
        #pdb.set_trace()

        return(new_templatestr)

    ## =============================
    def template_substitution(self, templatestr, entrykey, templatekey=None):
        '''
        Substitute database entry variables into template string.

        Parameters
        ----------
        templatestr : str
            The template string itself.
        entrykey : dict
            The key of the database entry from which to get fields to substitute into the template.
        templatekey : str
            If this template is for a special variable rather than an entrytype, then this key will tell which \
            special variable is being operated on.

        Returns
        -------
        templatestr : str
            The template string with all variables replaced.
        '''

        bibentry = self.bibdata[entrykey]

        ## Fill out the template if there is an implicit loop structure.
        template_has_implicit_index = True if re.search(self.implicit_index_pattern, templatestr) else False
        template_has_implicit_loop = True if '...' in templatestr else False
        if template_has_implicit_loop:
            ## In order to check if all of the variables use din an implicit loop are undefined, we make a template
            ## string in which all of the variables are replaced with "???", and check to see if the result equals
            ## that.
            templatestr_all_undef = re.sub(r'<.*?>', self.options['undefstr'], templatestr, re.UNICODE)

        templatestr = self.fillout_implicit_indices(templatestr, entrykey, templatekey)

        if (templatekey != None):
            is_nested = (templatekey in self.nested_templates)
        else:
            is_nested = (bibentry['entrytype'] in self.nested_templates)
        variables = re.findall(r'<.*?>', templatestr)

        ## Don't call the nested version of removing template option brackets if you don't have to, because it has to
        ## do significant extra work.
        if is_nested:
            templatestr = self.remove_nested_template_options_brackets(templatestr, bibentry, variables)
        else:
            templatestr = self.remove_template_options_brackets(templatestr, bibentry, variables)

        var_options = {}

        ## Go ahead and replace all of the template variables with the corresponding fields.
        for var in variables:
            if (var not in templatestr): continue

            varname = var[1:-1]     ## remove angle brackets to extract just the name

            ## The "title" variable has to be treated specially to deal with punctuation conflicts.
            if varname.startswith('title') and ('title' in bibentry):
                templatestr = self.insert_title_into_template(var, templatestr, bibentry)
                continue
            elif varname.startswith('citealpha'):
                ## Before we parse the template string to remove any undefined variables, we need to make sure that
                ## the entry has all the proper variables in it.
                templatestr = templatestr.replace(var, create_citation_alpha(bibentry, self.options))
                continue
            elif varname.startswith('citealnum'):
                ## The "citealphanum" style has to be handled outside of the usual specials loop --- it requires
                ## that *all* of the citelist be fully defined before it can start.
                continue

            ## If the variable contains a function asking for initials, then one tricky part is that the "middle"
            ## name part of a name dictionary can have multiple elements, so that each one needs to be initialed
            ## independently (and a period would thus need to be added to each separately). Note that "var_options"
            ## has to be kept separate from "options".
            idx = templatestr.index(var)
            if (idx + len(var) > 10):
                period_after_initial = (templatestr[idx+len(var)-10:idx+len(var)+1] == 'initial()>.') or \
                                       (templatestr[idx+len(var)-16:idx+len(var)+1] == 'initial().tie()>.')
                var_options.update({'period_after_initial':period_after_initial})
            else:
                var_options.update({'period_after_initial':False})

            ## Get the result of querying the variable in the entry. This will replace the template variable.
            res = self.get_variable(bibentry, varname, options=var_options)

            if (res == None):
                templatestr = templatestr.replace(var, self.options['undefstr'])
            elif isinstance(res, (list,dict)):
                ## If the object is a list and not a string, then we need to return it immediately, since the
                ## steps below assume a string.
                return(res)
            elif template_has_implicit_index and (self.options['undefstr'] in res):
                templatestr = templatestr.replace(var, self.options['undefstr'])
            else:
                templatestr = templatestr.replace(var, res)

        ## If the template uses an implicit loop, check if all variables were undefined. If none are defined, then the
        ## whole template should be returned as undefined.
        if template_has_implicit_loop:
            if (templatestr == templatestr_all_undef):
                return(None)

        ## Now that we've replaced template variables, go ahead and replace the special commands. We need to replace
        ## the hash symbol too because that indicates a comment when placed inside a template string.
        if (r'{\makeopenbracket}' in templatestr):
            templatestr = templatestr.replace(r'{\makeopenbracket}', '[')
        if (r'{\makeclosebracket}' in templatestr):
            templatestr = templatestr.replace(r'{\makeclosebracket}', ']')
        if (r'{\makeverticalbar}' in templatestr):
            templatestr = templatestr.replace(r'{\makeverticalbar}', '|')
        if (r'{\makegreaterthan}' in templatestr):
            templatestr = templatestr.replace(r'{\makegreaterthan}', '>')
        if (r'{\makelessthan}' in templatestr):
            templatestr = templatestr.replace(r'{\makelessthan}', '<')
        if (r'{\makehashsign}' in templatestr):
            templatestr = templatestr.replace(r'{\makehashsign}', '\\#')
        if (r'{\makeellipsis}' in templatestr):
            templatestr = templatestr.replace(r'{\makeellipsis}', '...')

        return(templatestr)

    ## ===================================
    def insert_title_into_template(self, title_var, templatestr, bibentry):
        '''
        Insert the title field into a template string.

        This requires more work than simply performing a string replacement, because there can be punctuation conflicts
        when the title itself ends with punctuation, while the template itself has punctuation immediately following the
        title.

        Parameters
        ----------
        title_var : str
            The title variable (which may simply be "<title>", or may have operators attached to the variable name.
        templatestr : str
            The template to insert the title into.
        bibentry : dict
            The bibliography entry to get the title from.

        Returns
        -------
        templatestr : str
            The template with the variable replaced with the "title" field, with possible operators applied.
        '''

        title = self.get_variable(bibentry, title_var[1:-1])
        if (title == None):
            return(templatestr)

        ## If the template string has punctuation right after the title, and the title itself also has punctuation,
        ## then you may get something like "Title?," where the two punctuation marks conflict. In that case, keep
        ## the title's punctuation and drop the template's.
        if title.endswith(('?','!')):
            idx = templatestr.index(title_var)
            if (templatestr[idx + len(title_var)] in (',','.','!','?',';',':')):
                templatestr = templatestr[:idx+len(title_var)] + templatestr[idx+1+len(title_var):]

        templatestr = templatestr.replace(title_var, title)

        return(templatestr)

    ## =============================
    def remove_nested_template_options_brackets(self, templatestr, entry, variables):
        '''
        Given a template string, go through each options sequence [...] and search for undefined variables. In each
        sequence, return only the block of each sequence in which all variables are defined (i.e. with outer braces
        removed).

        Parameters
        ----------
        templatestr : str
            The string defining the template to analyze.
        entry : dict
            The bibliography database entry inside which to look for variables.
        variables : list of str
            The variables to look for.
        '''

        while ('[' in templatestr):
            levels = get_delim_levels(templatestr, ('[',']'))

            ## If there is no nesting left then go ahead and parse the remaining string.
            if (2 not in levels):
                templatestr = self.remove_template_options_brackets(templatestr, entry, variables)
                return(templatestr)

            ## Find the start and end indices of all top-level option sequences.
            start_idx = []
            end_idx = []
            if (levels[0] == 1):
                start_idx.append(0)
            for i in range(1,len(levels)):
                if (levels[i] == 1) and (levels[i-1] == 0):
                    start_idx.append(i)
                if (levels[i] == 0) and (levels[i-1] == 1):
                    end_idx.append(i)

            ## To keep the code tractable, just work with the first pair of (start_idx,end_idx) values, rather than looping
            ## through every pair in the string. We can catch the next pair in the next pass through the loop.
            substr = templatestr[start_idx[0]+1:end_idx[0]]
            blocks = toplevel_split(substr, '|', levels)
            newblocks = []
            for block in blocks:
                block_variables = re.findall(r'<.*?>', block)
                newblock = self.remove_nested_template_options_brackets(block, entry, block_variables)
                if (newblock not in ('',None)):
                    newblocks.append(newblock)

            new_substr = '|'.join(newblocks)
            res = self.simplify_template_bracket(new_substr, entry, variables)
            templatestr = templatestr[:start_idx[0]] + res + templatestr[end_idx[0]+1:]

        return(templatestr)

    ## =============================
    def remove_template_options_brackets(self, templatestr, entry, variables):
        '''
        Given a template string, go through each options sequence [...] and search for undefined variables. In each
        sequence, return only the block of each sequence in which all variables are defined.

        Parameters
        ----------
        templatestr : str
            The string defining the template to analyze.
        entry : dict
            The bibliography database entry inside which to look for variables.
        variables : list of str
            The variables to look for.
        '''

        num_obrackets = templatestr.count('[')

        ## Do a nested search. From the beginning of the formatting string look for the first '[', and the first ']'. If
        ## they are out of order, raise an exception. Note that this assumes that the square brackets cannot be nested.
        for i in range(num_obrackets):
            start_idx = templatestr.index('[')
            end_idx = templatestr.index(']')
            if not (start_idx < end_idx):
                msg = 'A closed bracket "]" occurs before an open bracket "[" in the format ' + \
                      'string "' + templatestr + '"'
                raise SyntaxError(msg)

            ## Remove the outer square brackets, and use the resulting substring as an input to the parser.
            substr = templatestr[start_idx+1:end_idx]

            ## In each options train, go through and replace the whole train with the one block that has a defined value.
            res = self.simplify_template_bracket(substr, entry, variables)
            templatestr = templatestr[:start_idx] + res + templatestr[end_idx+1:]

        return(templatestr)

    ## =============================
    def simplify_template_bracket(self, templatestr, bibentry, variables):
        '''
        From an "options train" `[...|...|...]`, find the first fully defined block in the sequence.

        A style template string contains grammatical features of the form `[...|...|...]`, which we can call options
        sequences. Each "block" in the sequence (divided from the others by a `|` symbol), contains fields which, if
        defined, replace the entire options sequence in the returned string.

        When the options sequence ends with "|]" (i.e. at least one of the blocks is required to be defined) but we
        find that none of the blocks have all their variables defined, then we replace the entire block with the
        "undefstr".

        Parameters
        ----------
        templatestr : str
            The string containing a complete entrytype bibliography style template.
        variables : list of str
            The list of variables defined within the template string.
        bibentry : dict
            An entry from the bibliography database.

        Returns
        -------
        arg : str
              The string giving the entrytype block to replace an options sequence.

        Example
        -------
        simplify_template_bracket() is given an options sequence "[<title>|<booktitle>]" that contains two blocks. The code looks
        into the bibliography entry and does not find a "title" entry but does find a "booktitle" entry. So, the function
        returns "<booktitle>", without square brackets, thereby replacing the sequence with the proper defined variable.
        '''

        block_sequence = templatestr.split('|')

        ## Go through the if/elseif/else train of blocks within the string one by one. In each block, see if there are
        ## any variables defined. If no variables are present, then the block is "defined" and we return that block
        ## (i.e. replacing the train with that block). If an argument is defined, strip its surrounding '<' and '>' and
        ## look to see if the variable is defined in the bibdata entry. If so, the variable is defined and we return
        ## the '<var>' version of the variable (later code will do the variable replacement). If the variable is
        ## undefined (not present in the bibdata entry) then skip to the next block. If there is no next block, or if
        ## the block is empty (which means undefined by definition) then set the result to be the "undefined string".
        for block in block_sequence:
            if (block == ''):
                arg = self.options['undefstr']
                break

            ## If no variable exists inside the options-block, then just copy the text inside the block.
            if ('<' not in block):
                arg = block
                break

            ## Construct a list of the unique variables in the block.
            block_variables = list(set([v for v in variables if v in block]))

            ## Loop through the list of variables and find which ones are defined within the bibliography entry. If any
            ## variables within the block are undefined, then return an empty string.
            foundit = False
            for var in block_variables:
                varname = var[1:-1]             ## remove the angle brackets
                res = self.get_variable(bibentry, varname)
                foundit = ((res != None) and (res != self.options['undefstr']))
                if not foundit:
                    break

            ## If after going through all of the variables in a block, we have located definitions for all of them,
            ## then the entire block is defined, and we can return it without evaluating the next block.
            if foundit:
                arg = block
                break
            else:
                arg = ''

        return(arg)

    ## =============================
    def get_variable(self, bibentry, variable, options={}):
        '''
        Get the variable (i.e. entry field) from within the current bibliography entry.

        Parameters
        ----------
        bibentry : dict
            The bibliography entry to search.
        variable : str
            The dot-indexed template variable to evaluate.
        options : dict
            An optional dictionary giving extra info (such as whether to insert dots after initials).

        Returns
        -------
        result : str
            The field value (if it exists). If no corresponding field is found, return `None`.
        '''

        ## If there is no dot-indexer in the variable name, then return the entry field corresponding to the variable,
        ## if it exists in the entry.
        if ('.' not in variable):
            if (variable not in bibentry):
                return(None)
            elif (bibentry[variable] == None):
                return(None)
            else:
               return(unicode(bibentry[variable]))

        ## If there *is* a dot-indexer in the variable name, then we have to do some parsing. First we check the
        ## leftmost part (the field being indexed). If that doesn't exist then we're done --- the variable is
        ## undefined.
        var_parts = variable.split('.')
        if (var_parts[0] in bibentry):
            fieldname = var_parts[0]
        else:
            return(None)

        ## When using the "uniquify" operator, we need to be able to tell it the variable name. Use the "options"
        ## dictionary to get the variable's name into the "get_indexed_variable()" function, so we don't need to
        ## add an extra input variable.
        if ('.uniquify(' in variable):
            options.update({'varname':fieldname})

        indexer = '.' + '.'.join(var_parts[1:])
        result = self.get_indexed_variable(bibentry[fieldname], indexer, bibentry['entrykey'], options=options)

        return(result)

    ## =============================
    def get_indexed_variable(self, field, indexer, entrykey='', options={}):
        '''
        Get the result of dot-indexing into a field. This can be accessing an element of a list or dictionary, or the result
        of operating on a string with a function.

        Parameters
        ----------
        field : str
            The field to operate on.
        indexer : str
            The dot-delimited indexing operator.
        entrykey : str
            The entrykey of the bibliography entry being evaluated (useful for error messages).
        options : dict
            An optional dictionary giving extra info (such as whether to insert dots after initials).

        Returns
        -------
        result : str
            The string resulting from the dot-indexing operation on the field. If a valid operation cannot be performed,\
            then return "None".

        Example
        -------
        dict1 = {'first':'John', 'middle':'A', 'last':'Smith'}
        dict2 = {'first':'Ramsey', 'middle':'M Z', 'last':'Taylor'}
        field = [dict1, dict2]
        get_indexed_variable(field, '0.last.initial()')
        >>> S
        get_indexed_variable(field, '1.first')
        >>> Ramsey
        '''

        ## We need to split the string by the "dot" character, but **not** when the dot lies between a pair of parentheses ---
        ## that means that it's part of an operator argument!
        index_elements = indexer.split('.')
        index_elements = [i for i in index_elements if i]
        nelements = len(index_elements)

        ## If the indexing element is an integer, then we assume that it wants a list or tuple. If it finds one, then get the indexed item.
        if index_elements[0].isdigit():
            if not isinstance(field, (tuple, list)):
                fieldname = '' if not isinstance(field, str) else '"' + field + '" '
                indexname = index_elements[0]
                msg = 'Warning 029a: the ' + fieldname + 'field of entry ' + entrykey + ' is not a list and thus is ' + \
                      'not indexable by "' + indexname + '". Aborting template substitution'
                bib_warning(msg, disable=self.disable)
                return(None)
            else:
                newfield = field[int(index_elements[0])]
                if (nelements == 1):
                    return(newfield)
                else:
                    newindexer = '.' + '.'.join(index_elements[1:])
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))

        ## If the thing to the right of the dot-indexer is a *function*, then map the field to the function.
        if ('(' in index_elements[0]):
            if indexer.startswith('.initial()'):
                options['french_initials'] = False
                newfield = initialize_name(field, options=options)
                newindexer = indexer[10:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.frenchinitial()'):
                options['french_initials'] = True
                newfield = initialize_name(field, options=options)
                newindexer = indexer[16:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.compress()'):
                newfield = field.replace(' ','')
                newindexer = indexer[11:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.tie()'):
                newfield = field.replace(' ','~')
                newindexer = indexer[6:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.sentence_case()'):
                newfield = sentence_case(field)
                newindexer = indexer[16:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.ordinal()'):
                newfield = get_edition_ordinal(field, disable=None)
                newindexer = indexer[10:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.monthname()'):
                if field in self.monthnames:
                    newfield = self.monthnames[field]
                else:
                    newfield = field
                newindexer = indexer[12:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.monthabbrev()'):
                if field in self.monthabbrevs:
                    newfield = self.monthabbrevs[field]
                else:
                    newfield = field
                newindexer = indexer[14:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.to_namelist()'):
                sep = self.options['name_separator']
                newfield = namefield_to_namelist(field, key=entrykey, sep=sep, disable=self.disable)
                newindexer = indexer[14:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.format_authorlist()'):
                newfield = format_namelist(field, nametype='author', options=self.options)
                newindexer = indexer[20:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.format_editorlist()'):
                newfield = format_namelist(field, nametype='editor', options=self.options)
                newindexer = indexer[20:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.lower()'):
                newfield = purify_string(field).lower()
                newindexer = indexer[8:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.upper()'):
                newfield = purify_string(field).upper()
                newindexer = indexer[8:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.zfill('):
                match = re.search(r'.zfill\(.*\)', indexer, re.UNICODE)
                end_idx = match.end(0)
                result = match.group(0)[7:-1]
                if result:
                    nzeros = int(result)
                else:
                    nzeros = 0
                if str_is_integer(field) and (int(field) < 0):
                    newfield = '-' + str(field[1:]).zfill(nzeros)
                else:
                    newfield = str(field).zfill(nzeros)
                newindexer = indexer[end_idx:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.replace('):
                match = re.search(r'.replace\(.*\)', indexer, re.UNICODE)
                end_idx = match.end(0)
                result = match.group(0)[9:-1]
                (old, new) = result.split(',')
                if (old in field):
                    newfield = field.replace(old, new)
                else:
                    newfield = field

                newindexer = indexer[end_idx:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.purify()'):
                newfield = purify_string(field)
                newindexer = indexer[9:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif (index_elements[0] == 'uniquify(1)'):
                if (options['varname'] not in self.uniquify_vars):
                    self.uniquify_vars[options['varname']] = []

                newfield = field + '1'
                if (field+'1' in self.uniquify_vars[options['varname']]):
                    q = 2
                    while True:
                        newfield = field + str(q)
                        q += 1
                        if (newfield not in self.uniquify_vars[options['varname']]):
                            break
                self.uniquify_vars[options['varname']].append(newfield)
                #print('varname=%s, field=%s, newfield=%s' % (options['varname'], field, newfield))
                if (nelements == 1):
                    return(newfield)
                else:
                    newindexer = '.'.join(index_elements[1:])
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif (index_elements[0] == 'uniquify(a)'):
                if (options['varname'] not in self.uniquify_vars):
                    self.uniquify_vars[options['varname']] = []

                newfield = field
                if (field in self.uniquify_vars[options['varname']]):
                    q = 1
                    while True:
                        if (i < 27):
                            newfield = field + chr(q+96)               ## 97 == 'a', 98 == 'b', etc.
                        elif (i < 52):
                            newfield = field + chr(q+96) + chr(q+96)   ## double up if a single append doesn't work
                        elif (i < 78):
                            newfield = field + chr(q+96) + chr(q+96) + chr(q+96)   ## triple up if necessary
                        newfield += str(q)
                        q += 1
                        if (newfield not in self.uniquify_vars[options['varname']]):
                            break
                self.uniquify_vars[options['varname']].append(newfield)
                print('varname=%s, field=%s, newfield=%s' % (options['varname'], field, newfield))
                if (nelements == 1):
                    return(newfield)
                else:
                    newindexer = '.'.join(index_elements[1:])
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.if_singular('):
                match = re.search(r'.if_singular\(.*\)', indexer, re.UNICODE)
                end_idx = match.end(0)
                result = match.group(0)[13:-1]      ## remove function name and parentheses
                (variable_to_eval, singular_form, plural_form) = result.split(',')

                if (variable_to_eval not in self.bibdata[entrykey]):
                    newfield = ''
                elif (len(self.bibdata[entrykey][variable_to_eval]) == 1):
                    suffix = self.options[singular_form.strip()]
                    newfield = field + suffix
                else:
                    suffix = self.options[plural_form.strip()]
                    newfield = field + suffix

                newindexer = indexer[end_idx:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.if_equals('):
                match = re.search(r'.if_equals\(.*\)', indexer, re.UNICODE)
                end_idx = match.end(0)
                result = match.group(0)[11:-1]      ## remove function name and parentheses
                (test_str, then_form, else_form) = result.split(',')

                if (field == test_str):
                    newfield = then_form
                else:
                    newfield = else_form

                newindexer = indexer[end_idx:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            elif indexer.startswith('.remove_leading_zeros()'):
                newfield = field.lstrip('0')
                newindexer = indexer[23:]
                if (nelements == 1) or (newindexer == ''):
                    return(newfield)
                else:
                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))


#            elif indexer.startswith('.if_length_equals('):
#                match = re.search(r'.if_length_equals\(.*\)', indexer, re.UNICODE)
#                end_idx = match.end(0)
#                result = match.group(0)[18:-1]      ## remove function name and parentheses
#                (variable_to_eval, test_length, var_if_equals, var_if_notequals) = result.split(',')
#                #pdb.set_trace()
#
#                if (variable_to_eval not in self.bibdata[entrykey]):
#                    newfield = ''
#                elif (len(self.bibdata[entrykey][variable_to_eval]) == int(test_length)):
#                    suffix = self.options[var_if_equals.strip()]
#                    newfield = field + suffix
#                else:
#                    suffix = self.options[var_if_notequals.strip()]
#                    newfield = field + suffix
#
#                newindexer = indexer[end_idx:]
#                if (nelements == 1) or (newindexer == ''):
#                    return(newfield)
#                else:
#                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
#            elif indexer.startswith('.if_length_less_than('):
#                match = re.search(r'.if_length_less_than\(.*\)', indexer, re.UNICODE)
#                end_idx = match.end(0)
#                result = match.group(0)[21:-1]      ## remove function name and parentheses
#                (variable_to_eval, test_length, var_if_lessthan, var_if_notlessthan) = result.split(',')
#
#                if (variable_to_eval not in self.bibdata[entrykey]):
#                    newfield = ''
#                elif (len(self.bibdata[entrykey][variable_to_eval]) == int(test_length)):
#                    suffix = self.options[var_if_lessthan.strip()]
#                    newfield = field + suffix
#                else:
#                    suffix = self.options[var_if_notlessthan.strip()]
#                    newfield = field + suffix
#
#                newindexer = indexer[end_idx:]
#                if (nelements == 1) or (newindexer == ''):
#                    return(newfield)
#                else:
#                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
#            elif indexer.startswith('.if_length_more_than('):
#                match = re.search(r'.if_length_more_than\(.*\)', indexer, re.UNICODE)
#                end_idx = match.end(0)
#                result = match.group(0)[21:-1]      ## remove function name and parentheses
#                (variable_to_eval, test_length, var_if_morethan, var_if_notmorethan) = result.split(',')
#
#                if (variable_to_eval not in self.bibdata[entrykey]):
#                    newfield = ''
#                elif (len(self.bibdata[entrykey][variable_to_eval]) == int(test_length)):
#                    suffix = self.options[var_if_morethan.strip()]
#                    newfield = field + suffix
#                else:
#                    suffix = self.options[var_if_notmorethan.strip()]
#                    newfield = field + suffix
#
#                newindexer = indexer[end_idx:]
#                if (nelements == 1) or (newindexer == ''):
#                    return(newfield)
#                else:
#                    return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))
            #else:
            #    msg = 'Warning 029c: the template for entry ' + entrykey + ' has an unknown function ' + \
            #          '"' + index_elements[0] + '". Aborting template substitution'
            #    bib_warning(msg, disable=self.disable)
            #    return(None)

        ## If the indexer is a numerical range...
        if re.search(r'^.-?\d*:-?\d*', indexer, re.UNICODE):
            indexer = indexer[1:]   ## remove the leading period
            match = re.search(r'^.-?\d*:-?\d*', indexer, re.UNICODE)
            (start_idx,end_idx) = match.group(0).split(':')
            start_idx = int(start_idx)
            end_idx = int(end_idx)
            if (start_idx < 0):
                start_idx -= 1

            if (end_idx == -1):
                newfield = field[start_idx:end_idx] + field[end_idx]
            else:
                newfield = field[start_idx:end_idx+1]
            newindexer = indexer[int(match.end(0))+1:]

            if (nelements == 1) or (newindexer == ''):
                return(newfield)
            else:
                return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))

        if isinstance(field, str):
            return(field)

        ## If the thing to the right of the dot-indexer is a string, then we have to assume that it is an index into a
        ## dictionary. Check if the field is a dict type.
        if not isinstance(field, dict):
            fieldname = '' if not isinstance(field, str) else '"' + field + '" '
            indexname = index_elements[0]
            msg = 'Warning 029d: the ' + fieldname + 'field of entry ' + entrykey + ' is not a dictionary and thus is ' + \
                  'not indexable by "' + indexname + '". Aborting template substitution'
            bib_warning(msg, disable=self.disable)
            return(None)
        elif (index_elements[0] not in field):
            return(None)
        else:
            newfield = field[index_elements[0]]
            if (nelements == 1):
                return(newfield)
            else:
                newindexer = '.' + '.'.join(index_elements[1:])
                return(self.get_indexed_variable(newfield, newindexer, entrykey, options=options))

        ## The code should never reach here!
        msg = 'Warning 029e: Invalid field type error. Aborting template substitution'
        bib_warning(msg, disable=self.disable)
        return(None)

    ## ===================================
    def get_indexed_vars_in_template(self, templatestr):
        '''
        Get a list of the indexed variables within a template.

        Parameters
        ----------
        templatestr : str
            The template to analyze.

        Returns
        -------
        indexed_vars : list of str
            The list of variable names that are indexed variables.
        '''

        variables = re.findall(r'<.*?>', templatestr)
        indexed_vars = []
        for v in variables:
            found_indexed_var = re.findall(self.index_pattern, v)
            if found_indexed_var:
                varname = v[1:-1]
                if (varname not in indexed_vars):
                    indexed_vars.append(varname)

        return(indexed_vars)


## ================================================================================================
## END OF BIBDATA CLASS.
## ================================================================================================

## ===================================
def sentence_case(s):
    '''
    Reduce the case of the string to lower case, except for the first character in the string, and except if any given
    character is at nonzero brace level.

    Parameters
    ----------
    s : str
        The string to be modified.

    Returns
    -------
    t : str
        The resulting modified string.
    '''

    if ('{' not in s):
        return(s.lower().capitalize())

    ## Next we look for LaTeX commands, given by a backslash followed by a non-word character. Do not reduce those
    ## characters in the LaTeX command to lower case. To facilitate that, add one to the brace level for each of those
    ## character positions.
    brlevel = get_delim_levels(s)
    for match in re.finditer(r'\\\w+', s, re.UNICODE):
        (start,stop) = match.span()
        brlevel[start:stop] = [level+1 for level in brlevel[start:stop]]

    ## Convert the string to a character list for easy in-place modification.
    charlist = list(s)
    for i,c in enumerate(charlist):
        if (brlevel[i] == 0):
            charlist[i] = c.lower()

    charlist[0] = charlist[0].upper()
    t = ''.join(charlist)

    return(t)

## ===================================
def stringsplit(s, sep=r' |(?<!\\)~'):
    '''
    Split a string into tokens, taking care not to allow the separator to act unless at brace level zero.

    Parameters
    ----------
    s : str
        The string to split.

    Returns
    -------
    tokens : list of str
        The list of tokens.
    '''

    ## The item separating the name tokens can be either a space character or a tilde, if the tilde is not preceded by a
    ## backslash (in which case it instead represents an accent character and not a separator).
    if ('{' not in s):
        tokens = re.split(sep, s)
    else:
        z = get_delim_levels(s)
        indices = []
        for match in re.finditer(sep, s):
            (i,j) = match.span()
            if (z[i] == 0):
                ## Record the indices of the start and end of the match.
                indices.append((i,j))

        ntokens = len(indices)
        tokens = []
        if (ntokens == 0):
            tokens.append(s)
        if (ntokens > 0) and (indices[0][0] > 0):
            tokens.append(s[:indices[0][0]])

        ## Go through each match's indices and split the string at each.
        for n in xrange(ntokens):
            if (n == ntokens-1):
                j = indices[n][1]            ## the end of *this* separator
                tokens.append(s[j:])
            else:
                nexti = indices[n+1][0]      ## the beginning of the *next* separator
                j = indices[n][1]            ## the end of *this* separator
                tokens.append(s[j:nexti])

    return(tokens)

## =============================
def namefield_to_namelist(namefield, key=None, sep='and', disable=None):
    '''
    Parse a name field ("author" or "editor") of a BibTeX entry into a list of dicts, one for each person.

    Parameters
    ----------
    namefield : str
        Either the "author" field of a database entry or the "editor" field.
    key : str, optional
        The bibliography data entry key.
    sep : str, optional
        The string defining what to use as a name separator.
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    namelist : list
        A list of dictionaries, with one dictionary for each name. Each dict has keys "first", "middle", "prefix", \
        "last", and "suffix". The "last" key is the only one that is required.
    '''

    namefield = namefield.strip()
    namelist = []
    sep_pattern = re.compile(r'\s'+sep+'\s', re.UNICODE)

    ## Look for common typos.
    if re.search(r'\s'+sep+',\s', namefield, re.UNICODE):
        bib_warning('Warning 017a: The name string in entry "' + unicode(key) + '" has " '+sep+', ", which is likely a'
             ' typo. Continuing on anyway ...', disable)
    if re.search(r', '+sep, namefield, re.UNICODE):
        bib_warning('Warning 017b: The name string in entry "' + unicode(key) + '" has ", '+sep+'", which is likely a'
             ' typo. Continuing on anyway ...', disable)
    if re.search(r'\s'+sep+'\s+'+sep+'\s', namefield, re.UNICODE):
        bib_warning('Warning 017c: The name string in entry "' + unicode(key) + '" has two "'+sep+'"s separated by spaces, '
             'which is likely a typo. Continuing on anyway ...', disable)
        ## Replace the two "and"s with just one "and".
        namefield = re.sub(r'(?<=\s)'+sep+'\s+'+sep+'(?=\s)', namefield, sep, re.UNICODE)

    ## Split the string of names into individual strings, one for each complete name. Here we can split on whitespace
    ## surround the word "and" so that "{and}" and "word~and~word" will not allow the split. Need to treat the case of a
    ## single author separate from that of multiple authors in order to return a single-element *list* rather than a
    ## scalar.
    if not re.search(sep_pattern, namefield):
        namedict = namestr_to_namedict(namefield, disable)
        namelist.append(namedict)
    else:
        if '{' not in namefield:
            names = re.split(sep_pattern, namefield.strip())
        else:
            ## If there are braces in the string, then we need to be careful to only allow splitting of the names when
            ## ' and ' is at brace level 0. This requires replacing re.split() with a bunch of low-level code.
            z = get_delim_levels(namefield, ('{','}'))
            separators = []

            for match in re.finditer(sep_pattern, namefield):
                (i,j) = match.span()
                if (z[i] == 0):
                    ## Record the indices of the start and end of the match.
                    separators.append((i,j))

            num_names = len(separators)
            names = []
            if (num_names == 0):
                names.append(namefield.strip())
            if (num_names > 0) and (separators[0][0] > 0):
                names.append(namefield[:separators[0][0]].strip())

            ## Go through each match's indices and split the string at each.
            for n in xrange(num_names):
                if (n == num_names-1):
                    j = separators[n][1]            ## the end of *this* separator
                    names.append(namefield[j:].strip())
                else:
                    nexti = separators[n+1][0]      ## the beginning of the *next* separator
                    j = separators[n][1]            ## the end of *this* separator
                    names.append(namefield[j:nexti].strip())

        nauthors = len(names)
        for i in range(nauthors):
            namedict = namestr_to_namedict(names[i], disable)
            namelist.append(namedict)

    return(namelist)

## ===================================
def initialize_name(name, options=None, debug=False):
    '''
    From an input name element (first, middle, prefix, last, or suffix) , convert it to its initials.

    Parameters
    ----------
    name : str
        The name element to be converted.
    options : dict of bools, optional
        'french_intials': whether to initialize digraphs with two letters instead of the default of one.\
            For example, if use_french_initials==True, then "Christian" -> "Ch.", not "C.".
        'period_after_initial': whether to include a '.' after the author initial.

    Returns
    -------
    new_name : str
        The name element converted to its initials form.
    '''

    if (name == ''):
        return(name)
    if (options == None): options = {}
    if ('period_after_initial' not in options): options['period_after_initial'] = False
    if ('french_initials' not in options): options['french_initials'] = False
    if ('{' in name) and ('}' in name):
        name = purify_string(name)

    ## Go through the author's name elements and truncate the first and middle names to their initials. If using French
    ## initials, then a hyphenated name produces hyphenated initials (for example "Jean-Paul" -> "J.-P." and not "J."),
    ## and a name beginning with a digraph produces a digraph initial, so that Philippe -> Ph. (not P.), and
    ## Christian -> Ch. (not C.).
    digraphs = ('Ch','Gn','Ll','Ph','Ss','Th')
    period = '.' if options['period_after_initial'] else ''

    ## Split the name by spaces (primarily used for middle name strings, which may have multiple names in them), and
    ## remove any empty list elements produced by the split. Also remove any parenthetical names (such as used for
    ## nicknames).
    nametokens = list(name.split(' '))
    nametokens = [x for x in nametokens if x and not (x.startswith('(') or x.endswith(')') or x.startswith('[') or x.endswith(']'))]

    for j,token in enumerate(nametokens):
        if ('{' in token) and ('}' in token):
            token = purify_string(token)

        if ('-' in token):
            ## If the name is hyphenated, then initialize the hyphenated parts of it, and assemble the result by
            ## combining initials with the hyphens. That is, "Chein-Ing" -> "C.-I.".
            pieces = token.split('-')
            nametokens[j] = (period+'-').join([initialize_name(p, options) for p in pieces])
        else:
            ## If the token already ends in a period then it might already be an initial, but only if it has length 2.
            ## Otherwise you still need to truncate it. If the name only has one character in it, then treat it as a
            ## full name that doesn't need initializing.
            if token.endswith('.') and (len(token) == 2):
                nametokens[j] = token[0] + period
            elif (len(token) > 1):
                if options['french_initials'] and (token[:2] in digraphs):
                    nametokens[j] = token[:2] + period
                else:
                    nametokens[j] = token[0] + period
            else:
                nametokens[j] = token

    newname = ' '.join(nametokens)

    if newname.endswith('.'):
        newname = newname[:-1]

    if debug: print('Initializer input [' + name + '] --> output [' + newname + ']')

    return(newname)

## ===================================
def get_delim_levels(s, delims=('{','}'), operator=None):
    '''
    Generate a list of level numbers for each character in a string.

    Parameters
    ----------
    s : str
        The string to characterize.
    delims : tuple of two strings
        The (left-hand-side delimiter, right-hand-side delimiter).
    operator : str
        The "operator" string that appears to the left of the delimiter. For example, operator=r'\textbf' allows the \
        code to look for nested structures like `{...}` and simultaneously for structures like `\textbf{...}`, and be \
        able to keep track of which is which.

    Returns
    -------
    levels : list of ints
        A list giving the operator delimiter level (or "brace level" if no operator is given) of each character in \
        the string.
    '''

    stack = []
    oplevels = [0]*len(s)        ## operator level
    brlevels = [0]*len(s)        ## brace level

    ## Locate the left-delimiters and increment the level each time we find one.
    if (operator != None) and (s.count(operator) < 1):
        return(oplevels)

    for j,c in enumerate(s):
        if (c == delims[0]):
            if (operator != None) and (s[j-len(operator):j] == operator):
                stack.append('o')       ## add an "operator" marker to the stack
            else:
                stack.append('b')       ## add a "brace level" marker to the stack
        elif (c == delims[1]):
            ## If the stack is empty but the delimiter level isn't resolved, then the braces are unbalanced.
            if not stack: return([])
            stack.pop()

        if (operator != None): oplevels[j] = stack.count('o')
        brlevels[j] = stack.count('b')

    if (operator != None):
        return(oplevels)
    else:
        return(brlevels)

## ===================================
def show_levels_debug(s, levels):
    '''
    A debugging tool for showing delimiter levels and the input string next to one another.

    Parameters
    ----------
    s : str
        The string used to determine the delimiter levels.
    levels : list of ints
        The list of delimiter levels at each character position in the string.
    '''
    q = 0   ## counter for the character ending a line
    if ('\n' in s):
        for line in s.split('\n'):
            print(line)
            print(unicode(levels[q:q+len(line)])[2:-1].replace(',','').replace(' ',''))
            q += len(line)
    else:
        print(s)
        print(unicode(levels)[1:-1].replace(',','').replace(' ',''))
    return

## ===================================
def get_quote_levels(s, disable=None, debug=False):
    '''
    Return a list which gives the "quotation level" of each character in the string.

    Parameters
    ----------
    s : str
        The string to analyze.
    disable : list of ints, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    alevels : list of ints
        The double-quote-level for (``,'') pairs in the string.
    blevels : list of ints
        The single-quote-level for (`,') pairs in the string.
    clevels : list of ints
        The neutral-quote-level for (",") pairs in the string.

    Notes
    -----
    When using double-quotes, it is easy to break the parser, so they should be used only sparingly.
    '''

    stack = []
    alevels = [0]*len(s)        ## double-quote level
    blevels = [0]*len(s)        ## single-quote level
    clevels = [0]*len(s)        ## neutral-quote level

    for j,ch in enumerate(s):
        if (ch == '`') and (s[j-1] != '\\'):
            ## Note: the '\\' case here is for detecting a grave accent markup.
            if (s[j:j+2] == '``'):
                stack.append('a')       ## add a double-quote marker to the stack
            elif (s[j-1] != '`') and (s[j-1].isspace() or (s[j-1] in '()[]{}":;,<>') or (j == 0)):
                ## The trouble with single-quotes is the clash with apostrophes. So, only increment the single-quote
                ## counter if we think it is the start of a quote (not immediately preceded by a non-whitespace
                ## character).
                stack.append('b')       ## add a single-quote marker to the stack
        elif (ch == "'") and (alevels[j-1]+blevels[j-1]+clevels[j-1] > 0) and (s[j-1] != '\\'):
            ## Note: the '\\' case here is for detecting an accent markup.
            if (s[j:j+2] == "''") and (stack[-1] == 'a'):
                stack.pop()    ## remove double-quote marker from the stack
            elif (s[j-1] != "'") and (stack[-1] == 'b'):
                stack.pop()    ## remove single-quote marker from the stack
        elif (ch == '"') and (s[j-1] != '\\'):
            ## Note: the '\\' here case is for not detecting an umlaut markup.
            if (len(stack) > 0) and (stack[-1] == 'c'):
                stack.pop()    ## remove neutral-quote marker from the stack
            else:
                stack.append('c')

        alevels[j] = stack.count('a')
        blevels[j] = stack.count('b')
        clevels[j] = stack.count('c')

    if (alevels[-1] > 0):
        bib_warning('Warning 018a: found mismatched "``"..."''" quote pairs in the input string "' + s + \
             '". Ignoring the problem and continuing on ...', disable)
        alevels[-1] = 0
    if (blevels[-1] > 0):
        bib_warning('Warning 018b: found mismatched "`"..."\'" quote pairs in the input string "' + s + \
             '". Ignoring the problem and continuing on ...', disable)
        blevels[-1] = 0
    if (clevels[-1] > 0):
        bib_warning('Warning 018c: found mismatched "..." quote pairs in the input string "' + s + \
             '". Ignoring the problem and continuing on ...', disable)
        clevels[-1] = 0

    if debug:
        show_levels_debug(s, alevels)
        show_levels_debug(s, blevels)
        show_levels_debug(s, clevels)

    return(alevels, blevels, clevels)

## ===================================
def splitat(s, ilist):
    '''
    Split a string at locations given by a list of indices.

    This can be used more flexibly than Python's native string split() function, when the character you are splitting on
    is not always a valid splitting location.

    Parameters
    ----------
    s : str
        The string to split.
    ilist : list
        The list of string index locations at which to split the string.

    Returns
    -------
    slist : list of str
        The list of split substrings.

    Example
    -------
    s = splitat('here.but.not.here', [4,8])
    >>> ['here', 'but', 'not.here']
    '''

    numsplit = len(ilist)
    slist = []
    ilist.sort()

    ## If the function is being asked to "split" at the first character, then just truncate.
    if (ilist[0] == 0):
        s = s[1:]
        ilist = ilist[1:]
        numsplit -= 1

    ## If the function is being asked to "split" at the last character, then just truncate.
    if (ilist[-1] == (len(s)-1)):
        s = s[:-1]
        ilist = ilist[:-1]
        numsplit -= 1

    ## If truncation has removed all of the "splitting" locations from the list, then return.
    if (numsplit == 0):
        return(s, '')

    start = 0
    end = len(s)
    slist.append(s[:ilist[0]])

    if (len(ilist) == 1):
        slist.append(s[ilist[0]+1:])
    elif (len(ilist) > 1):
        for n in range(numsplit-1):
            start = ilist[n] + 1
            end = ilist[n+1]
            slist.append(s[start:end])
        slist.append(s[ilist[-1]+1:])

    return(slist)

## =============================
def multisplit(s, seps):
    '''
    Split a string using more than one separator.

    Copied from http://stackoverflow.com/questions/1059559/python-strings-split-with-multiple-separators.

    Parameters
    ----------
    s : str
        The string to split.
    sep : list of str
        The list of separators.

    Returns
    -------
    res : list
        The list of split substrings.
    '''

    res = [s]
    for sep in seps:
        (s, res) = (res, [])
        for seq in s:
            res += seq.split(sep)
    return(res)

## ===================================
def enwrap_nested_string(s, delims=('{','}'), odd_operator=r'\textbf', even_operator=r'\textrm', disable=None):
    '''
    This function will return the input string if it finds there are no nested operators inside (i.e. when the number of
    delimiters found is < 2).

    Parameters
    ----------
    s : str
        The string whose nested operators are to be modified.
    delims : tuple of two strings
        The left and right delimiters for all matches.
    odd_operator : str
        The nested operator (applied to the left of the delimiter) currently used within string "s".
    even_operator : str
        The operator used to replace the currently used one for all even nesting levels.
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    s : str
        The modified string.
    '''
    if not (odd_operator in s):
        return(s)

    oplevels = get_delim_levels(s, delims, odd_operator)
    if (oplevels[-1] > 0):
        bib_warning('Warning 019: found mismatched "{","}" brace pairs in the input string. Ignoring the problem and'
             ' continuing on ...', disable)
        return(s)

    ## In the operator queue, we replace all even-numbered levels while leaving all odd-numbered levels alone. Recall
    ## that "oplevels" encodes the position of the *delimiter* and not the position of where the operator starts.
    maxlevels = max(oplevels)
    if (maxlevels < 2):
        return(s)

    ## Select only even levels starting at 2. "q" is a counter for the number of substr replacements.
    q = 0
    shift = len(odd_operator) - len(even_operator)
    for i,level in enumerate(oplevels):
        if (level > 0) and (level % 2 == 0):
            ## Any place we see a transition from one level lower to this level is a substr we want to replace. The
            ## "shift" used here is to compensate for changes in the length of the string due to differences in length
            ## between the input operator and output.
            if (oplevels[i-1] < level):
                #print(i, level, oplevels[i-1], s, s[:i-len(odd_operator)], s[i:])
                s = s[:i-len(odd_operator)-(q*shift)] + even_operator + s[i-(q*shift):]
                q += 1

    return(s)

## ===================================
def enwrap_nested_quotes(s, disable=None, debug=False):
    '''
    Find nested quotes within strings and, if necessary, replace them with the proper nesting (i.e. outer quotes use
    ````...''`` while inner quotes use ```...'``).

    Parameters
    ----------
    s : str
        The string to modify.
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    s : str
        The new string in which nested quotes have been properly reformatted.
    '''

    ## NOTE: There is quite a lot going on in this function, so it may help future development to write some of this
    ## work into subroutines.

    ## First check for cases where parsing is going to be very complicated. For now, we should just flag these cases to
    ## inform the user that they need to modify the source to tell the parser what they want to do.
    if ("```" in s) or ("'''" in s):
        bib_warning('Warning 020: the input string ["' + s + '"] contains multiple unseparated quote characters.'
             ' Bibulous cannot unnest the single and double quotes from this set, so the separate quotations must be '
             ' physically separated like ``{\:}``, for example. Ignoring the quotation marks and continuing ...',
             disable)
        return(s)

    ## Note that a backtick preceded by a backslash, an explamation point, or a question mark, indicates LaTeX markup
    ## for a grave accent, an inverted explamation point, and an inverted question mark, respectively.
    #adelims = ('``',"''")
    anum = len(re.findall(r'(?<!\!\?\\)``', s))
    #bdelims = ('`',"'")
    bnum = len(re.findall(r'(?<!\!\?\\)`', s))
    #cdelim = '"'
    cnum = len(re.findall(r'(?<!\\)"', s))
    if ((anum + bnum + cnum) <= 1) and (r'\enquote{' not in s):
        return(s)

    ## Get the lists describing the quote nesting.
    (alevels, blevels, clevels) = get_quote_levels(s, disable=disable, debug=debug)

    ## First, we look at the quote stack and replace *all* quote pairs with \enquote{...}. When done, we can use
    ## `enwrap_nested_string()` to replace the odd and even instances of \enquote{} with different quotation markers,
    ## depending on locale. `q` is the amount of shift between indices in the current string and those in the source
    ## string.
    q = 0
    for i in range(len(s)):
        if (i == 0) and (alevels[0] == 1):
            ## This is a transition up in level. Add "\enquote{".
            s = s[:i+q] + r'\enquote{' + s[i+2+q:]
            q += len(r'\enquote{') - 2
        elif (i > 0) and (alevels[i-1] < alevels[i]):
            ## This is a transition up in level. Add "\enquote{".
            s = s[:i+q] + r'\enquote{' + s[i+2+q:]
            q += len(r'\enquote{') - 2
        elif (i > 0) and (alevels[i-1] > alevels[i]):
            ## This is a transition down in level. Add "}".
            s = s[:i+q] + '}' + s[i+2+q:]
            q -= 1

        ## Do the same thing for single quotes.
        if (i == 0) and (blevels[0] == 1):
            ## This is a transition up in level. Add "\enquote{".
            s = s[:i+q] + r'\enquote{' + s[i+1+q:]
            q += len(r'\enquote{') - 1
        elif (i > 0) and (blevels[i-1] < blevels[i]):
            ## This is a transition up in level. Add "\enquote{".
            s = s[:i+q] + r'\enquote{' + s[i+1+q:]
            q += len(r'\enquote{') - 1
        elif (i > 0) and (blevels[i-1] > blevels[i]):
            ## This is a transition down in level. Add "}".
            s = s[:i+q] + '}' + s[i+1+q:]

        ## Do the same thing for neutral quotes.
        if (i == 0) and (clevels[0] == 1):
            ## This is a transition up in level. Add "\enquote{".
            s = s[:i+q] + r'\enquote{' + s[i+1+q:]
            q += len(r'\enquote{') - 1
        elif (i > 0) and (clevels[i-1] < clevels[i]):
            ## This is a transition up in level. Add "\enquote{".
            s = s[:i+q] + r'\enquote{' + s[i+1+q:]
            q += len(r'\enquote{') - 1
        elif (i > 0) and (clevels[i-1] > clevels[i]):
            ## This is a transition down in level. Add "}".
            s = s[:i+q] + '}' + s[i+1+q:]

    ## Next, we determine the nesting levels of quotations.
    qlevels = get_delim_levels(s, ('{','}'), r'\enquote')

    ## Finally, replace odd levels of quotation with "``" and even levels with "`". The approach taken below works for
    ## the American convention. Need to generalize this behavior for British convention, and, even more broadly, to all
    ## locale-dependent quotation mark behavior.
    t = 0
    odd_operators = ("``","''")
    even_operators = ("`","'")

    if debug:
        show_levels_debug(s, qlevels)

    for i,level in enumerate(qlevels):
        if (qlevels[i-1] == 0) and (level == 0): continue

        ## Any place we see a transition from one level lower to this level is a substr we want to replace. The shift
        ## "t" used here is to compensate for changes in the length of the string due to differences in length between
        ## the input operator and output. Also, if we are about to substitute in a quote character (or two, in the case
        ## of LaTeX double quotes), then we need to be careful to look in front and see if the quotes butt up against
        ## one another, in which case we need to add a small space. For example, LaTeX will interpret ''' as a double
        ## ending quote followed by a single ending quote, even ifwe meant it to be the other way around. The space
        ## "\:" will remove the ambiguity.

        ## There is quite a lot going on in this loop, so it may help future work to replace some of the operations
        ## here with subroutines.
        if (level % 2 == 0):
            if (i < len(r'\enquote{')-1) or (qlevels[i-1] < level):
                left = i + t - len(r'\enquote{') + 1
                right = i + t + 1
                if (i > len(odd_operators[0])):
                    needs_space = (s[left-len(odd_operators[0]):left] == odd_operators[0])
                else:
                    needs_space = False

                if needs_space:
                    newstr = r'\:' + even_operators[0]
                else:
                    newstr = even_operators[0]

                s = s[:left] + newstr + s[right:]
                t += len(newstr) - len(r'\enquote{')
            elif (qlevels[i-1] > level):
                left = i + t - len('}') + 1
                right = i + t + 1
                if (i > len(even_operators[1])):
                    needs_space = (s[left-len(even_operators[1]):left] == even_operators[1])
                else:
                    needs_space = False

                if needs_space:
                    newstr = r'\:' + odd_operators[1]
                else:
                    newstr = odd_operators[1]

                s = s[:left] + newstr + s[right:]
                t += len(newstr) - len('}')
        else:
            if (i < len('r\enquote{')-1) or (qlevels[i-1] < level):
                left = i + t - len(r'\enquote{') + 1
                right = i + t + 1
                if (i > len(even_operators[0])):
                    needs_space = (s[left-len(even_operators[0]):left] == even_operators[0])
                else:
                    needs_space = False

                if needs_space:
                    newstr = r'\:' + odd_operators[0]
                else:
                    newstr = odd_operators[0]

                s = s[:left] + newstr + s[right:]
                t += len(newstr) - len(r'\enquote{')
            elif (qlevels[i-1] > level):
                left = i + t - len('}') + 1
                right = i + t + 1
                if (i > len(odd_operators[1])):
                    needs_space = (s[left-len(odd_operators[1]):left] == odd_operators[1])
                else:
                    needs_space = False

                if needs_space:
                    newstr = r'\:' + even_operators[1]
                else:
                    newstr = even_operators[1]

                s = s[:left] + newstr + s[right:]
                t += len(newstr) - len('}')

    return(s)

## =============================
def purify_string(s):
    '''
    Remove the LaTeX-based formatting elements from a string so that a sorting function can use alphanumerical sorting
    on the string.

    Parameters
    ----------
    s : str
        The string to "purify".

    Returns
    -------
    p : str
        The "purified" string.
    '''

    p = unicode(s)
    if not ('\\' in p):
        ## If there are no LaTeX commands, then just remove any braces present.
        p = p.replace('{', '')
        p = p.replace('}', '')
        return(p)

    ## If the string contains mathematical markup (i.e. $...$), then we have to treat that case specially, since we
    ## don't want to run "purify" on mathematics --- it's not as easy as simply replacing math markup with unicode
    ## equivalents. So, if we find math markup then we split the string into math parts and non-math parts, purify the
    ## non-math ones, and then piece it back together. Messy.
    mathpattern = re.compile(r'(?<!\\)\$.*?(?<!\\)\$', re.UNICODE)
    matchobj = re.search(r'(?<!\\)\$.*?(?<!\\)\$', s, re.UNICODE)

    if matchobj:
        start_idx = []
        end_idx = []

        for matchobj in re.finditer(mathpattern, s):
            (start,end) = matchobj.span()
            start_idx.append(start)
            end_idx.append(end)

        idx = sorted(list(set(start_idx + end_idx)))
        if (idx[0] != 0):
            idx = [0] + idx
        if (idx[-1] != len(s)):
            idx = idx + [len(s)]

        p = ''
        for i in range(len(idx)-1):
            if (s[idx[i]] != '$'):
                p += purify_string(s[idx[i]:idx[i+1]])
            else:
                p += s[idx[i]:idx[i+1]]
    else:
        ## Convert any LaTeX character encodings directly to their unicode equivalents.
        p = latex_to_utf8(p)

        ## Next we look for LaTeX commands. LaTeX variables will have the form "\variable" followed by either
        ## whitespace, '{', or '}'. A function will have the form "\functionname{...}" where the ellipsis can be
        ## anything.
        match = re.compile(r'\\\w+', re.UNICODE)
        p = match.sub('', p)

        ## Finally, remove the braces used for LaTeX commands. We can't just replace '{' and '}' wholesale, since the
        ## syntax allows '\{' and '\}' to produce text braces. So first we remove the command braces, and then we swap
        ## '\{' for '{' etc at the end.
        match = re.compile(r'(?<!\\){', re.UNICODE)
        p = match.sub('', p, re.UNICODE)
        match = re.compile(r'(?<!\\)}', re.UNICODE)
        p = match.sub('', p, re.UNICODE)
        p = p.replace('\\{', '{')
        p = p.replace('\\}', '}')

    return(p)

## =============================
def latex_to_utf8(s):
    '''
    Translate LaTeX-markup special characters to their Unicode equivalents.

    Parameters
    ----------
    s : str
        The string to translate.

    Returns
    -------
    s : str
        The translated version of the input.
    '''

    ## Note that the code below uses replace() loops rather than a translation table, since the latter only supports
    ## one-to-one translation, whereas something more flexible is needed here.
    if ('\\' not in s):
        return(s)

    ## First, some easy replacements.
    trans = {r'\$':'$', r'\%':'%', r'\_':'_', r'\&':'&', r'\#':'#', r'!`':'¡', r'?`':'¿'}
    for c in trans:
        if c in s: s = s.replace(c, trans[c])

    ## If there are any double backslashes, place some braces around them to prevent something like "\\aa" from getting
    ## interpreted as a backslash plus "\aa". This makes the string easier to parse and does no harm.
    if r'\\' in s:
        s = s.replace(r'\\',r'{\\}')

    ## First identify all the LaTeX special characters in the string, then replace them all with their Unicode
    ## equivalents. (This is to make sure that they alphabetize correctly for sorting.) The translation dictionary
    ## below uses single-letter accent commands, such as \u{g}. These commands are one of (r'\b', r'\c', r'\d', r'\H',
    ## r'\k', r'\r', r'\u', r'\v'), followed by an open brace, a single character, and a closed brace. These
    ## replacements are done first because some of the special characters use '\i', which would otherwise get replaced
    ## by the "dotless i" Unicode character, and so the replacement dictionary here would not detect the proper LaTeX
    ## code for it.

    ## First, characters with a cedilla or comma below.
    if (r'\c' in s):
        trans = {r'\c{C}':'Ç', r'{\c C}':'Ç', r'\c{c}':'ç', r'{\c c}':'ç', r'\c{E}':'Ȩ', r'{\c E}':'Ȩ',
                 r'\c{e}':'ȩ', r'{\c e}':'ȩ', r'\c{G}':'Ģ', r'{\c G}':'Ģ', r'\c{g}':'ģ', r'{\c g}':'ģ',
                 r'\c{K}':'Ķ', r'{\c K}':'Ķ', r'\c{k}':'ķ', r'{\c k}':'ķ', r'\c{L}':'Ļ', r'{\c L}':'Ļ',
                 r'\c{l}':'ļ', r'{\c l}':'ļ', r'\c{N}':'Ņ', r'{\c N}':'Ņ', r'\c{n}':'ņ', r'{\c n}':'ņ',
                 r'\c{R}':'Ŗ', r'{\c R}':'Ŗ', r'\c{r}':'ŗ', r'{\c r}':'ŗ', r'\c{S}':'Ş', r'{\c S}':'Ş',
                 r'\c{s}':'ş', r'{\c s}':'ş', r'\c{T}':'Ţ', r'{\c T}':'Ţ', r'\c{t}':'ţ', r'{\c t}':'ţ'}

        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Characters with breve above. Note that the "\u" is problematic when "unicode_literals" is turned on via
    ## "from __future__ import unicode_literals". Thus, in the block below, rather than raw strings with single
    ## backslashes, we have to use double-backslashes.
    if ('\\u' in s):
        trans = {'\\u{A}':'Ă', '{\\u A}':'Ă', '\\u{a}':'ă',  '{\\u a}':'ă', '\\u{E}':'Ĕ', '{\\u E}':'Ĕ',
                 '\\u{e}':'ĕ', '{\\u e}':'ĕ', '\\u{G}':'Ğ',  '{\\u G}':'Ğ', '\\u{g}':'ğ', '{\\u g}':'ğ',
                 '\\u{I}':'Ĭ', '{\\u I}':'Ĭ', '\\u{\i}':'ĭ', '{\\u\i}':'ĭ', '\\u{O}':'Ŏ', '{\\u O}':'Ŏ',
                 '\\u{o}':'ŏ', '{\\u o}':'ŏ', '\\u{U}':'Ŭ',  '{\\u U}':'Ŭ', '\\u{u}':'ŭ', '{\\u u}':'ŭ'}

        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Characters with an ogonek.
    if (r'\k' in s):
        trans = {r'\k{A}':'Ą', r'{\k A}':'Ą', r'\k{a}':'ą', r'{\k a}':'ą', r'\k(E}':'Ę', r'{\k E}':'Ę',
                 r'\k{e}':'ę', r'{\k e}':'ę', r'\k{I}':'Į', r'{\k I}':'Į', r'\k{i}':'į', r'{\k i}':'į',
                 r'\k{O}':'Ǫ', r'{\k O}':'Ǫ', r'\k{o}':'ǫ', r'{\k o}':'ǫ', r'\k{U}':'Ų', r'{\k U}':'Ų',
                 r'\k{u}':'ų', r'{\k u}':'ų'}
        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Characters with hachek.
    if (r'\v' in s):
        trans = {r'\v{C}':'Č', r'{\v C}':'Č', r'\v{c}':'č', r'{\v c}':'č', r'\v{D}':'Ď', r'{\v D}':'Ď',
                 r'\v{d}':'ď', r'{\v d}':'ď', r'\v{E}':'Ě', r'{\v E}':'Ě', r'\v{e}':'ě', r'{\v e}':'ě',
                 r'\v{L}':'Ľ', r'{\v L}':'Ľ', r'\v{l}':'ľ', r'{\v l}':'ľ', r'\v{N}':'Ň', r'{\v N}':'Ň',
                 r'\v{n}':'ň', r'{\v n}':'ň', r'\v{R}':'Ř', r'{\v R}':'Ř', r'\v{r}':'ř', r'{\v r}':'ř',
                 r'\v{S}':'Š', r'{\v S}':'Š', r'\v{s}':'š', r'{\v s}':'š', r'\v{T}':'Ť', r'{\v T}':'Ť',
                 r'\v{t}':'ť', r'{\v t}':'ť', r'\v{Z}':'Ž', r'{\v Z}':'Ž', r'\v{z}':'ž', r'{\v z}':'ž',
                 r'\v{H}':'\u021E', r'{\v H}':'\u021E', r'\v{h}':'\u021F',  r'{\v h}':'\u021F',
                 r'\v{A}':'\u01CD', r'{\v A}':'\u01CD', r'\v{a}':'\u01CE',  r'{\v a}':'\u01CE',
                 r'\v{I}':'\u01CF', r'{\v I}':'\u01CF', r'\v{\i}':'\u01D0', r'{\v \i}':'\u01D0',
                 r'\v{O}':'\u01D1', r'{\v O}':'\u01D1', r'\v{o}':'\u01D2',  r'{\v o}':'\u01D2',
                 r'\v{U}':'\u01D3', r'{\v U}':'\u01D3', r'\v{u}':'\u01D4',  r'{\v u}':'\u01D4',
                 r'\v{G}':'\u01E6', r'{\v G}':'\u01E6', r'\v{g}':'\u01E7',  r'{\v g}':'\u01E7',
                 r'\v{K}':'\u01E8', r'{\v K}':'\u01E8', r'\v{k}':'\u01E9',  r'{\v k}':'\u01E9'}
        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    if (r'\H' in s):
        trans = {r'\H{O}':u'Ő',  r'\H{o}':u'ő',  r'\H{U}':u'Ű',  r'\H{u}':u'ű', r'{\H O}':u'Ő', r'{\H o}':u'ő',
                 r'{\H U}':u'Ű', r'{\H u}':u'ű'}
        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Characters with a ring above.
    if (r'\r' in s):
        trans = {r'\r{U}':u'Ů', r'{\r U}':u'Ů', r'\r{u}':u'ů', r'{\r u}':u'ů'}
        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Now let's do the straightforward accent characters.
    trans = {r'\`A':u'\u00C1',  r'\`a':u'\u00E0',  r"\'A":u'\u00C1',  r"\'a":u'\u00E1',  r'\~A':u'\u00C3',
             r'\^a':u'\u00E2',  r'\"A':u'\u00C4',  r'\~a':u'\u00E3',  r'\"a':u'\u00E4',  r'\`E':u'\u00C8',
             r"\'E":u'\u00C9',  r'\`e':u'\u00E8',  r'\^E':u'\u00CA',  r"\'e":u'\u00E9',  r'\"E':u'\u00CB',
             r'\^e':u'\u00EA',  r'\`I':u'\u00CC',  r'\"e':u'\u00EB',  r"\'I":u'\u00CD',  r'\`\i':u'\u00EC',
             r'\^I':u'\u00CE',  r"\'\i":u'\u00ED', r'\"I':u'\u00CF',  r'\^\i':u'\u00EE', r'\~N':u'\u00D1',
             r'\"\i':u'\u00EF', r'\`O':u'\u00D2',  r'\~n':u'\u00F1',  r"\'O":u'\u00D3',  r'\`o':u'\u00F2',
             r'\^O':u'\u00D4',  r"\'o":u'\u00F3',  r'\~O':u'\u00D5',  r'\^o':u'\u00F4',  r'\"O':u'\u00D6',
             r'\~o':u'\u00F5',  r'\"o':u'\u00F6',  r'\`U':u'\u00D9',  r"\'U":u'\u00DA',  r'\`u':u'\u00F9',
             r'\^U':u'\u00DB',  r"\'u":u'\u00FA',  r'\"U':u'\u00DC',  r'\^u':u'\u00FB',  r"\'Y":u'\u00DD',
             r'\"u':u'\u00FC',  r"\'y":u'\u00FD',  r'\"y':u'\u00FF',  r'\=A':u'\u0100',  r'\=a':u'\u0101',
             r"\'C":u'\u0106',  r"\'c":u'\u0107',  r'\^C':u'\u0108',  r'\^c':u'\u0109',  r'\.C':u'\u010A',
             r'\.c':u'\u010B',  r'\=E':u'\u0112',  r'\=e':u'\u0113',  r'\.E':u'\u0116',  r'\.e':u'\u0117',
             r'\^G':u'\u011C',  r'\^g':u'\u011D',  r'\.G':u'\u0120',  r'\.g':u'\u0121',  r'\^H':u'\u0124',
             r'\^h':u'\u0125',  r'\~I':u'\u0128',  r'\~\i':u'\u0129', r'\=I':u'\u012A',  r'\=\i':u'\u012B',
             r'\.I':u'\u0130',  r'\^J':u'\u0134',  r'\^\j':u'\u0135', r"\'L":u'\u0139',  r"\'N":u'\u0143',
             r"\'n":u'\u0144',  r'\=O':u'\u014C',  r'\=o':u'\u014D',  r"\'R":u'\u0154',  r"\'r":u'\u0155',
             r"\'S":u'\u015A',  r"\'s":u'\u015B',  r'\~U':u'\u0168',  r'\~u':u'\u0169',  r'\=U':u'\u016A',
             r'\=u':u'\u016B',  r'\^W':u'\u0174',  r'\^w':u'\u0175',  r'\^Y':u'\u0176',  r'\^y':u'\u0177',
             r"\'Z":u'\u0179',  r"\'z":u'\u017A',  r'\.Z':u'\u017B',  r'\.z':u'\u017C',  r'\`Y':u'Ỳ',
             r'\`y':u'ỳ',       r"\'K":u'Ḱ',       r"\'k":u'ḱ',       r"\'l":u'ĺ',       r'\^A':u'Â',
             r'\^S':u'Ŝ',       r'\^s':u'ŝ',       r'\"Y':u'Ÿ',       r'\~E':u'Ẽ',       r'\~e':u'ẽ',
             r'\~Y':u'Ỹ',       r'\~y':u'ỹ'}

    for c in trans:
        if c in s: s = s.replace(c, trans[c])

    ## Do again for anyone using extra braces.
    trans = {r'\`{A}':u'\u00C1',  r'\`{a}':u'\u00E0',  r"\'{A}":u'\u00C1',  r"\'{a}":u'\u00E1',  r'\~{A}':u'\u00C3',
             r'\^{a}':u'\u00E2',  r'\"{A}':u'\u00C4',  r'\~{a}':u'\u00E3',  r'\"{a}':u'\u00E4',  r'\`{E}':u'\u00C8',
             r"\'{E}":u'\u00C9',  r'\`{e}':u'\u00E8',  r'\^{E}':u'\u00CA',  r"\'{e}":u'\u00E9',  r'\"{E}':u'\u00CB',
             r'\^{e}':u'\u00EA',  r'\`{I}':u'\u00CC',  r'\"{e}':u'\u00EB',  r"\'{I}":u'\u00CD',  r'\`{\i}':u'\u00EC',
             r'\^{I}':u'\u00CE',  r"\'{\i}":u'\u00ED', r'\"{I}':u'\u00CF',  r'\^{\i}':u'\u00EE', r'\~{N}':u'\u00D1',
             r'\"{\i}':u'\u00EF', r'\`{O}':u'\u00D2',  r'\~{n}':u'\u00F1',  r"\'{O}":u'\u00D3',  r'\`{o}':u'\u00F2',
             r'\^{O}':u'\u00D4',  r"\'{o}":u'\u00F3',  r'\~{O}':u'\u00D5',  r'\^{o}':u'\u00F4',  r'\"{O}':u'\u00D6',
             r'\~{o}':u'\u00F5',  r'\"{o}':u'\u00F6',  r'\`{U}':u'\u00D9',  r"\'{U}":u'\u00DA',  r'\`{u}':u'\u00F9',
             r'\^{U}':u'\u00DB',  r"\'{u}":u'\u00FA',  r'\"{U}':u'\u00DC',  r'\^{u}':u'\u00FB',  r"\'{Y}":u'\u00DD',
             r'\"{u}':u'\u00FC',  r"\'{y}":u'\u00FD',  r'\"{y}':u'\u00FF',  r'\={A}':u'\u0100',  r'\={a}':u'\u0101',
             r"\'{C}":u'\u0106',  r"\'{c}":u'\u0107',  r'\^{C}':u'\u0108',  r'\^{c}':u'\u0109',  r'\.{C}':u'\u010A',
             r'\.{c}':u'\u010B',  r'\={E}':u'\u0112',  r'\={e}':u'\u0113',  r'\.{E}':u'\u0116',  r'\.{e}':u'\u0117',
             r'\^{G}':u'\u011C',  r'\^{g}':u'\u011D',  r'\.{G}':u'\u0120',  r'\.{g}':u'\u0121',  r'\^{H}':u'\u0124',
             r'\^{h}':u'\u0125',  r'\~{I}':u'\u0128',  r'\~{\i}':u'\u0129', r'\={I}':u'\u012A',  r'\={\i}':u'\u012B',
             r'\.{I}':u'\u0130',  r'\^{J}':u'\u0134',  r'\^{\j}':u'\u0135', r"\'{L}":u'\u0139',  r"\'{N}":u'\u0143',
             r"\'{n}":u'\u0144',  r'\={O}':u'\u014C',  r'\={o}':u'\u014D',  r"\'{R}":u'\u0154',  r"\'{r}":u'\u0155',
             r"\'{S}":u'\u015A',  r"\'{s}":u'\u015B',  r'\~{U}':u'\u0168',  r'\~{u}':u'\u0169',  r'\={U}':u'\u016A',
             r'\={u}':u'\u016B',  r'\^{W}':u'\u0174',  r'\^{w}':u'\u0175',  r'\^{Y}':u'\u0176',  r'\^{y}':u'\u0177',
             r"\'{Z}":u'\u0179',  r"\'{z}":u'\u017A',  r'\.{Z}':u'\u017B',  r'\.{z}':u'\u017C',  r'\`{Y}':u'Ỳ',
             r'\`{y}':u'ỳ',       r"\'{K}":u'Ḱ',       r"\'{k}":u'ḱ',       r"\'{l}":u'ĺ',       r'\^{A}':u'Â',
             r'\^{S}':u'Ŝ',       r'\^{s}':u'ŝ',       r'\"{Y}':u'Ÿ',       r'\~{E}':u'Ẽ',       r'\~{e}':u'ẽ',
             r'\~{Y}':u'Ỹ',       r'\~{y}':u'ỹ'}

    for c in trans:
        if c in s: s = s.replace(c, trans[c])

    ## Those were easy. Next we look for single-char codes that must be followed by a non-alpha element, so that for
    ## example \orange will produce the "\orange" LaTeX command while "{\o}range" or "\o range" will produce "ørange".
    ## Since we're using regex and not Python's string objects, we need to replace all backslashes with double-
    ## backslashes. Thankfully, no other regex escape characters occur in this list of LaTeX markup for foreign letters.
    trans = {r'\AA':u'Å', r'\AE':u'Æ', r'\aa':u'å', r'\ae':u'æ', r'\O':u'Ø',  r'\o':u'ø',
             r'\ss':u'ß', r'\i':u'ı',  r'\L':u'Ł',  r'\l':u'ł',  r'\OE':u'Œ', r'\oe':u'œ',
             r'\j':u'ȷ',  r'\P':u'¶',  r'\S':u'§',  r'\DH':u'Ð', r'\dh':u'ð', r'\DJ':u'Đ',
             r'\dj':u'đ', r'\IJ':u'Ĳ', r'\ij':u'ĳ', r'\NG':u'Ŋ', r'\ng':u'ŋ', r'\SS':u'ẞ',
             r'\TH':u'Þ', r'\th':u'þ'}

    for c in trans:
        match = re.compile(c.replace('\\','\\\\')+r'(?!\w)', re.UNICODE)
        s = match.sub(trans[c], s, re.UNICODE)

    return(s)

## =============================
def brace_split(string, splitter=" "):

    ## If there are braces in the string, then we need to be careful to only allow splitting of the names when
    ## ' and ' is at brace level 0. This requires replacing re.split() with a bunch of low-level code.
    z = get_delim_levels(string, ('{','}'))
    separators = []
    sep_pattern = re.compile(splitter, re.UNICODE)

    for match in re.finditer(sep_pattern, string):
        (i,j) = match.span()
        if (z[i] == 0):
            ## Record the indices of the start and end of the match.
            separators.append((i,j))

    num_splits = len(separators)
    splits = []
    if (num_splits == 0):
        splits.append(string.strip())
    if (num_splits > 0) and (separators[0][0] > 0):
        splits.append(string[:separators[0][0]].strip())

    ## Go through each match's indices and split the string at each.
    for n in xrange(num_splits):
        if (n == num_splits-1):
            j = separators[n][1]            ## the end of *this* separator
            splits.append(string[j:].strip())
        else:
            nexti = separators[n+1][0]      ## the beginning of the *next* separator
            j = separators[n][1]            ## the end of *this* separator
            splits.append(string[j:nexti].strip())
    return splits

## =============================

def namestr_to_namedict(namestr, disable=None):
    '''
    Take a BibTeX string representing a single person's name and parse it into its first, middle, last, etc pieces.

    BibTeX allows three different styles of author formats.
        (1) A space-separated list, [firstname middlenames suffix lastname]
        (2) A two-element comma-separated list, [prefix lastname, firstname middlenames]
        (3) a three-element comma-separated list, [prefix lastname, suffix, firstname middlenames].
    So, we can separate these three categories by counting the number of commas that appear.

    Parameters
    ----------
    namestr : str
        The string containing a single person's name, in BibTeX format
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    namedict : dict
        A dictionary with keys "first", "middle", "prefix", "last", and "suffix".
    '''

    namestr = namestr.strip()

    ## First, if there is a comma within the string, then build the delimiter level list so we can check whether the
    ## comma is at delimiter level 0 (and therefore a valid comma for determining name structure). Using this,
    ## determine the locations of "valid" commas.
    if (',' in namestr):
        z = get_delim_levels(namestr, ('{','}'))
        commapos = []
        for match in re.finditer(',', namestr):
            i = match.start()
            if (z[i] == 0): commapos.append(i)
    else:
        commapos = []

    ## Note: switch on "len(commapos)" here rather than on "(',' not in namestr)" because the latter will produce an
    ## error when the comma occurs at brace levels other than zero.
    if (len(commapos) == 0):
        ## Allow nametokens to be split by spaces *or* word ties ('~' == unbreakable spaces), except when the '~' is
        ## preceded by a backslash, in which case we have the LaTeX markup for the tilde accent. We use "stringsplit()"
        ## rather than the standard string object's "split()" function because we don't want the split to be applied
        ## when the separator is not at brace level zero.
        nametokens = stringsplit(namestr, r' |(?<!\\)~')

        for n in nametokens:
            n_temp = n.strip('{').strip('}')[:-1]
            ## If we find a dot which is not preceded by a backslash and not succeeded by a dash. Also, we shouldn't
            ## care about dots appearing within curle braces, so we have to check for that as well.
            z = get_delim_levels(namestr, ('{','}'))
            for match in re.finditer(r'(?<!\\)\.(?!-)', n_temp):
                i = match.start()
                j = match.end()
                if (z[i] == 0) and (namestr[j+1] != ')'):
                    bib_warning('Warning 021: The name token "' + n + '" in namestring "' + namestr + \
                         '" has a "." inside it, which may be a typo. Ignoring ...', disable)

        namedict = {}
        if (len(nametokens) == 1):
            namedict['last'] = nametokens[0]
        elif (len(nametokens) == 2):
            namedict['first'] = nametokens[0]
            namedict['last'] = nametokens[1]
        elif (len(nametokens) > 2):
            namedict['first'] = nametokens[0]
            namedict['last'] = nametokens[-1]
            namedict['middle'] = ' '.join(nametokens[1:-1])
            namedict = search_middlename_for_prefixes(namedict)

    elif (len(commapos) == 1):
        namedict = {}
        (firstpart, secondpart) = splitat(namestr, commapos)
        first_nametokens = brace_split(firstpart.strip(),' ')
        second_nametokens = brace_split(secondpart.strip(),' ')

        if (len(first_nametokens) == 1):
            namedict['last'] = first_nametokens[0]
        elif (len(first_nametokens) > 1):
            namedict['prefix'] = ' '.join(first_nametokens[0:-1])
            namedict['last'] = first_nametokens[-1]

        namedict['first'] = second_nametokens[0]
        if (len(second_nametokens) > 1):
            namedict['middle'] = ' '.join(second_nametokens[1:])
            namedict = search_middlename_for_prefixes(namedict)

    elif (len(commapos) == 2):
        namedict = {}
        (firstpart, secondpart, thirdpart) = splitat(namestr, commapos)
        first_nametokens = firstpart.strip().split(' ')
        second_nametokens = secondpart.strip().split(' ')
        third_nametokens = thirdpart.strip().split(' ')

        if (len(second_nametokens) != 1):
            bib_warning('Warning 022: the BibTeX format for namestr="' + namestr + '" is malformed.\nThere should ' + \
                 'be only one name in the second part of the three comma-separated name elements.', disable)
            return({'last':'???'})

        if (len(first_nametokens) == 1):
            namedict['last'] = first_nametokens[0]
        elif (len(first_nametokens) == 2):
            namedict['prefix'] = ' '.join(first_nametokens[0:-1])
            namedict['last'] = first_nametokens[-1]

        namedict['suffix'] = second_nametokens[0]
        namedict['first'] = third_nametokens[0]

        if (len(third_nametokens) > 1):
            namedict['middle'] = ' '.join(third_nametokens[1:])
            #if (len(namedict['middle']) == 1):
            #    namedict['middle'] = namedict['middle'][0]
            namedict = search_middlename_for_prefixes(namedict)

    elif (len(commapos) == 3):
        ## The name format is (first,middle,prefix,last).
        namedict = {}
        (firstpart, secondpart, thirdpart, fourthpart) = splitat(namestr, commapos)
        namedict['first'] = firstpart.strip()
        namedict['middle'] = secondpart.strip()
        namedict['prefix'] = thirdpart.strip()
        namedict['last'] = fourthpart.strip()
        #namedict['suffix'] =

    elif (len(commapos) == 4):
        ## The name format is (first,middle,prefix,last,suffix).
        namedict = {}
        (firstpart, secondpart, thirdpart, fourthpart, fifthpart) = splitat(namestr, commapos)
        namedict['first'] = firstpart.strip()
        namedict['middle'] = secondpart.strip()
        namedict['prefix'] = thirdpart.strip()
        namedict['last'] = fourthpart.strip()
        namedict['suffix'] = fifthpart.strip()

    else:
        bib_warning('Warning 023: the BibTeX format for namestr="' + namestr + '" is malformed.\nThere should ' + \
             'never be more than four commas in a given name.', disable)
        return({'last':'???'})

    ## If any tokens in the middle name start with lower case, then move them, and any tokens after them, to the prefix.
    ## An important difference is that prefixes typically don't get converted to initials when generating the formatted
    ## bibliography string.
    if ('middle' in namedict) and (namedict['middle'] != ''):
        nametokens = namedict['middle'].split(' ')
        if not isinstance(nametokens, list): nametokens = [nametokens]
        nametokens = [x for x in nametokens if x]
        move = False
        movelist = []
        removelist = []
        for i,t in enumerate(nametokens):
            if t[0].islower(): move = True
            if move:
                movelist.append(i)
                removelist.append(i)

        ## Add the tokens to the prefix and remove them from the middle name.
        if movelist:
            if ('prefix' not in namedict): namedict['prefix'] = ''
            movetokens = [t for i,t in enumerate(nametokens) if i in movelist]
            namedict['prefix'] = ' '.join(movetokens) + ' ' + namedict['prefix']
            namedict['prefix'] = namedict['prefix'].strip()
        if removelist:
            nametokens = [t for i,t in enumerate(nametokens) if i not in removelist]
            namedict['middle'] = ' '.join(nametokens)

    ## Finally, go through and remove any name elements that are blank. Use "key in namedict.keys()" rather than
    ## "key in namedict" here because we want to be able to change the dictionary in the loop.
    for key in namedict.keys():
        if (namedict[key].strip() == ''):
            del namedict[key]

    return(namedict)

## ===================================
def search_middlename_for_prefixes(namedict):
    '''
    From the middle name of a single person, check if any of the names should be placed into the "prefix" and move them
    there.

    Parameters
    ----------
    namedict : dict
        The dictionary containing the key "middle", containing the string with the person's middle names/initials.

    Returns
    -------
    namedict : dict
        The dictionary augmented with the key "prefix" if a prefix is indeed found.
    '''

    if ('middle' not in namedict):
        return(namedict)

    ## Search the list of middle names from the back to the front. If the name encountered starts with lower case, then
    ## it is moved to namedict['prefix']. If not, then stop the search and break out of the loop.
    middlenames = namedict['middle'].split(' ')
    prefix = []
    for m in middlenames[::-1]:
        if m and m[0].islower():
            prefix.append(middlenames.pop())
        else:
            break

    if prefix:
        namedict['prefix'] = ' '.join(prefix)
        namedict['middle'] = ' '.join(middlenames)

    return(namedict)

## =============================
def get_edition_ordinal(edition_field, disable=None):
    '''
    Given a bibliography entry's edition *number*, format it as an ordinal (i.e. "1st", "2nd" instead of "1", "2") in
    the way that it will appear on the formatted page.

    Parameters
    ----------
    edition_field : str
        The string representing the "edition" field in the database entry.
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    edition_ordinal_str : str
        The formatted form of the edition, with ordinal attached.
    '''

    ## First check that the field exists.
    if (edition_field == None):
        return(None)

    if not edition_field.isdigit():
        return(edition_field)

    trans = {'first':'1', 'second':'2', 'third':'3', 'fourth':'4', 'fifth':'5', 'sixth':'6', 'seventh':'7',
             'eighth':'8', 'ninth':'10', 'tenth':'10', 'eleventh':'11', 'twelfth':'12', 'thirteenth':'13',
             'fourteenth':'14', 'fifteenth':'15', 'sixteenth':'16', 'seventeenth':'17', 'eighteenth':'18',
             'nineteenth':'19', 'twentieth':'20'}

    if edition_field.lower() in trans:
        edition_field = trans[edition_field.lower()]

    ## Add the ordinal string to the number.
    if (edition_field == '0'):
        bib_warning('Warning 024: an edition number of "0" is invalid. Cannot create ordinal.', disable)
        return(edition_field)

    if (edition_field == '1'):
        edition_ordinal_str = '1st'
    elif (edition_field == '2'):
        edition_ordinal_str = '2nd'
    elif (edition_field == '3'):
        edition_ordinal_str = '3rd'
    elif (int(edition_field) > 3):
        edition_ordinal_str = edition_field + 'th'
    else:
        ## I'm not sure whether the code can reach this point, but just in case.
        edition_ordinal_str = edition_field

    return(edition_ordinal_str)

## =============================
def export_bibfile(bibdata, filename, abbrevs=None):
    '''
    Write a bibliography database dictionary into a .bib file.

    Parameters
    ----------
    filename : str
        The filename of the file to write.
    bibdata : dict
        The bibliography dictionary to write out.
    abbrevs : dict, optional
        The dictionary of abbreviations to write to the BIB file.
    '''

    assert isinstance(filename, basestring), 'Input "filename" must be a string.'
    filehandle = codecs.open(filename, 'w', 'utf-8')

    if ('preamble' in bibdata):
        filehandle.write(bibdata['preamble'])
        filehandle.write('\n\n')

    if (abbrevs != None):
        for abbrev in abbrevs:
            filehandle.write('@STRING{' + abbrev + ' = ' + abbrevs[abbrev] + '}\n')
        filehandle.write('\n')

    for key in bibdata:
        if (key == 'preamble'): continue

        ## Since you're about to delete an item from the "entry" dictionary, and it is a view into the main database
        ## dictionary, you need to make a deep copy of it first before deleteing or else it will delete the entry from
        ## the main database as well!
        entry = copy.deepcopy(bibdata[key])
        filehandle.write('@' + entry['entrytype'].upper() + '{' + key + ',\n')
        del entry['entrytype']
        nkeys = len(entry.keys())

        ## Write out the entries.
        for i,k in enumerate(entry):
            filehandle.write('  ' + k + ' = {' + unicode(entry[k]) + '}')

            ## If this is the last field in the dictionary, then do not end the line with a trailing comma.
            if (i == (nkeys-1)):
                filehandle.write('\n')
            else:
                filehandle.write(',\n')

        filehandle.write('}\n\n')

    filehandle.close()
    return

## =============================
def parse_pagerange(pages_str, citekey=None, disable=None):
    '''
    Given a string containing the "pages" field of a bibliographic entry, figure out the start and end pages.

    Parameters
    ----------
    pages_str : str
        The string to parse.
    citekey : str, optional
        The citation key (useful for debugging messages).
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    startpage : str
        The starting page.
    endpage : str
        The ending page. If endpage==startpage, then endpage is set to None.
    '''

    if not pages_str:
        return('','')

    ## Note that we work with strings instead of integers, because the use of letters in article pages is common
    ## (e.g. page "D5").
    if ('-' in pages_str) or (',' in pages_str):
        pagesplit = multisplit(pages_str, ('-',','))
        startpage = pagesplit[0].strip()
        endpage = pagesplit[-1].strip()
        if (endpage == startpage): endpage = None
    else:
        startpage = pages_str
        endpage = None

    ## For user convenience, add a check here that if endpage and startpage are both numbers and endpage <= startpage,
    ## then there is a typo.
    if startpage.isdigit() and endpage and endpage.isdigit():
        if int(endpage) < int(startpage):
            if (citekey != None):
                bib_warning('Warning 025a: the "pages" field in entry "' + citekey + '" has a malformed page range '
                     '(endpage < startpage). Ignoring ...', disable)
            else:
                bib_warning('Warning 025b: the "pages" field "' + pages_str + '" is malformed, since endpage < '
                     'startpage. Ignoring ...', disable)

    return(startpage, endpage)

## =============================
def parse_nameabbrev(abbrevstr):
    '''
    Given a string containing either a single "name" > "abbreviation" pair or a list of such pairs, parse the string
    into a dictionary of names and abbreviations.

    Parameters
    ----------
    abbrevstr : str
        The string containing the abbreviation definitions.

    Returns
    -------
    nameabbrev_dict : dict
        A dictionary with names for keys and abbreviations for values.
    '''

    nameabbrev_dict = {}
    abbrevlist = abbrevstr.split(',')
    for a in abbrevlist:
        pair = a.split(' > ')
        pair[0] = pair[0].strip()
        nameabbrev_dict[pair[0]] = pair[1].strip()

    return(nameabbrev_dict)

## =============================
def filter_script(line):
    '''
    Remove elements from a Python script which are provide the most egregious security flaws; also replace some
    identifiers with their correct namespace representation.

    Parameters
    ----------
    line : str
        The line of source code to filter.

    Returns
    -------
    filtered : str
        The filtered line of source code.
    '''

    line = line.strip()
    os_pattern = re.compile(r'\Wos.', re.UNICODE)
    sys_pattern = re.compile(r'\Wsys.', re.UNICODE)

    if line.startswith('import') or re.search(os_pattern, line) or re.search(sys_pattern, line):
        filtered = ''
    else:
        filtered = line

    ## Replace any use of "entry", "options", "citedict", or "bstdict" with the needed identifier
    ## for the namespace inside format_bibitem().
    filtered = re.sub(r'(?<=\W)entry(?=\W)', 'self.bibdata[c]', line, re.UNICODE)
    filtered = re.sub(r'(?<=\W)options(?=\W)', 'self.options', line, re.UNICODE)
    filtered = re.sub(r'(?<=\W)citedict(?=\W)', 'self.citedict', line, re.UNICODE)
    filtered = re.sub(r'(?<=\W)bstdict(?=\W)', 'self.bstdict', line, re.UNICODE)

    return(filtered)

## =============================
def str_is_integer(s):
    '''
    Check is an input string represents an integer value. Although a trivial function, it will be useful for user
    scripts.

    Parameters
    ----------
    s : str
        The input string to test.

    Returns
    -------
    is_integer : bool
        Whether the string represents an integer value.
    '''

    try:
        int(s)
        return(True)
    except ValueError:
        return(False)

## =============================
def bib_warning(msg, disable=None):
    '''
    Print a warning message, with the option to disable any given message.

    Parameters
    ----------
    msg : str
        The warning message to print.
    disable : list of int, optional
        The list of warning message numbers that the user wishes to disable (i.e. ignore).
    '''

    if (disable == None):
        print(msg)
        return

    ## For each number in the "ignore" list, find out if the warning message is one of the ones to ignore. If so, then
    ## do nothing.
    show_warning = True
    for i in disable:
        s = ('Warning %03i' % i)
        if msg.startswith(s):
            show_warning = False
            break

    if show_warning:
        print(msg)

    return

## =============================
def create_citation_alpha(entry, options):
    '''
    Create an "alpha" style citation key (typically the first three letters of the author's last name, followed by the
    last two numbers of the year).

    Parameters
    ----------
    entry : dict
        The bibliography entry.
    options : dict
        The dictionary of keyword options (the only key used is "name_separator").

    Returns
    -------
    alpha : str
        The alpha-style citation key.
    '''

    if ('authorlist' in entry):
        namelist = entry['authorlist']
    elif ('editorlist' in entry):
        namelist = entry['editorlist']
    elif ('author' in entry):
        namelist = namefield_to_namelist(entry['author'], sep=options['name_separator'])
    elif ('editor' in entry):
        namelist = namefield_to_namelist(entry['editor'], sep=options['name_separator'])
    elif ('organization' in entry):
        org = entry['organization']
        namelist = namefield_to_namelist(org, sep=options['name_separator'])
    elif ('institution' in entry):
        inst = entry['institution']
        namelist = namefield_to_namelist(inst, sep=options['name_separator'])
    else:
        return('UNDEFINED')

    ## Note: you need to run "purify" before extracting the first three letters, because the first character might be a
    ## curly brace that purify can get rid of, or the first three characters might be something like "\AA" which should
    ## be extracted as a single unicode character.
    if (len(namelist) == 1):
        concat_name = purify_string(namelist[0]['last'])[0:3]
    elif (len(namelist) > 1):
        concat_name = ''
        for name in namelist:
            concat_name += purify_string(name['last'].strip('{}'))[0]

    if ('year' in entry):
        year = entry['year'][-2:]
    else:
        year = '??'

    alpha = concat_name[0:3] + year

    return(alpha)

## =============================
def toplevel_split(s, splitchar, levels):
    '''
    Split a string, but only if the splitting character is at level 0 or 1 and not higher.

    Parameters
    ----------
    s : str
        The string to split.
    splitchar : str
        The character to split with.
    levels : list of ints
        The operator levels of the characters in the string.

    Returns
    -------
    split_list : list of str
        The list of split sections of the string.
    '''

    ## Make a complete list of indices where we can find the splitting character. Ignore those locations at operator
    ## levels of 2 or higher.
    pos = []
    for i,c in enumerate(s):
        if (c == splitchar) and (levels[i] < 2):
            pos.append(i)

    if (len(pos) > 0):
        split_list = splitat(s, pos)
    else:
        split_list = [s]

    return(split_list)

## ===================================
def get_variable_name_elements(variable):
    '''
    Split the variable name into "name" (left-hand-side part), "iterator" (middle part), and "remainder" (the right-
    hand-side part).

    With these three elements, we will know how to build a template variable inside the implicit loop.

    Parameters
    ----------
    variable : str
        The variable name to be parsed.

    Returns
    -------
    var_dict : dict
        The dictionary containing elements of the variable name, with keys 'varname', 'prefix', 'index', and 'suffix'. \
        The input variable can be reconstructed with name + '.' + prefix + index + suffix.
    '''

    varlist = variable.split('.')
    var_dict = {}
    var_dict['name'] = varlist[0]
    var_dict['index'] = ''
    var_dict['prefix'] = ''
    var_dict['suffix'] = ''

    for i,piece in enumerate(varlist[1:]):
        if piece.isdigit() or (piece == 'n') or (piece == 'N'):
            var_dict['index'] = piece
        elif (var_dict['index'] == ''):
            var_dict['prefix'] += piece + '.'
        else:
            var_dict['suffix'] += '.' + piece

    return(var_dict)

## ===================================
def get_names(entry, templatestr):
    '''
    Get the list of names associated with a given entry, giving priority to the first namelist
    present in the "namelists" list.

    Parameters
    ----------
    entry : dict
        The bibliography data entry.
    templatestr : str
        The template string -- to tell whether to use authors or editors.

    Returns
    -------
    namelist : list of dicts
        The list of names found.
    '''

    if ('authorname' in templatestr) and ('authorlist' in entry):
        return(entry['authorlist'])
    elif ('editorname' in templatestr) and ('editorlist' in entry):
        return(entry['editorlist'])

    return([])

## =============================
def format_namelist(namelist, nametype='author', options=None):
    '''
    Format a list of dictionaries (one dict for each person) into a long string, with the format according to the
    directives in the bibliography style template.

    Parameters
    ----------
    namelist : str
        The list of dictionaries containing all of the names to be formatted.
    nametype : str, {'author', 'editor'}, optional
        Whether the names are for authors or editors.
    options : dict, optional
        The dictionary of keyword-based options.

    Returns
    -------
    namestr : str
        The formatted form of the "name string". This is generally a list of authors or list of editors.
    '''

    if (options == None): options = {}
    if ('use_firstname_initials' not in options): options['use_firstname_initials'] = True
    if ('namelist_format' not in options):  options['namelist_format'] = 'first_name_first'
    if ('maxauthors' not in options):  options['maxauthors'] = 9
    if ('minauthors' not in options):  options['minauthors'] = 9
    if ('maxeditors' not in options):  options['maxeditors'] = 5
    if ('mineditors' not in options):  options['mineditors'] = 5
    if ('etal_message' not in options):  options['etal_message'] = '\\textit{et al.}'
    if ('use_name_ties' not in options):  options['use_name_ties'] = False
    if ('terse_inits' not in options):  options['terse_inits'] = False
    if ('french_intials' not in options):  options['french_intials'] = False
    if ('period_after_initial' not in options):  options['period_after_initial'] = True

    ## First get all of the options variables needed below, depending on whether the function is operating on a list of
    ## authors or a list of editors. Second, insert "authorlist" into the bibliography database entry so that other
    ## functions can have access to it. (This is the "author" or "editor" string parsed into individual names, so that
    ## each person's name is represented by a dictionary, and the whole set of names is a list of dicts.)
    if (nametype == 'author'):
        maxnames = options['maxauthors']
        minnames = options['minauthors']
    elif (nametype == 'editor'):
        maxnames = options['maxeditors']
        minnames = options['mineditors']

    ## This next block generates the list "namelist", which is a list of strings, with each element of `namelist` being
    ## a single author's name. That single author's name is encoded as a dictionary with keys "first", "middle",
    ## "prefix", "last", and "suffix".
    npersons = len(namelist)
    new_namelist = []
    for person in namelist:
        ## The BibTeX standard states that a final author in the authors field of "and others" should be taken as
        ## meaning to use \textit{et al.} at the end of the author list.
        if (person['last'].lower() == 'others') and ('first' not in person):
            npersons -= 1
            maxnames = npersons - 1
            continue

        ## From the person's name dictionary, create a string of the name in the format desired for the final BBL file.
        formatted_name = namedict_to_formatted_namestr(person, options=options)
        new_namelist.append(formatted_name)

    ## Now that we have the complete list of pre-formatted names, we need to join them together into a single string
    ## that can be inserted into the template.
    if (npersons == 1):
        namestr = new_namelist[0]
    elif (npersons == 2):
        namestr = ' and '.join(new_namelist)
    elif (npersons > 2) and (npersons <= maxnames):
        ## Make a string in which each person's name is separated by a comma, except the last name, which has a comma
        ## then "and" before the name.
        namestr = ', '.join(new_namelist[:-1]) + ', and ' + new_namelist[-1]
    elif (npersons > maxnames):
        ## If the number of names in the list exceeds the maximum, then truncate the list to the first "minnames" only,
        ## and add "et al." to the end of the string giving all the names.
        if (minnames == 1):
            namestr = new_namelist[0] + options['etal_message']
        else:
            namestr = ', '.join(new_namelist[:minnames]) + options['etal_message']
    else:
        raise ValueError('How did you get here?')

    ## Add a tag onto the end if describing an editorlist.
    if (nametype == 'editor'):
        if (npersons == 1):
            edmsg = ', ed.' if ('edmsg1' not in options) else options['edmsg1']
        else:
            edmsg = ', eds' if ('edmsg2' not in options) else options['edmsg2']
        namestr += edmsg

    return(namestr)

## =============================
def namedict_to_formatted_namestr(namedict, options=None):
    '''
    Convert a name dictionary into a formatted name string.

    Parameters
    ----------
    namedict : dict
        The name dictionary (contains a required key "last" and optional keys "first", "middle", "prefix", and "suffix".
    options : dict, optional
        Dictionary of formatting options.

    Returns
    -------
    namestr : str
        The formatted string of the name.
    '''

    if (options == None): options = {}
    if ('use_firstname_initials' not in options): options['use_firstname_initials'] = True
    if ('namelist_format' not in options):  options['namelist_format'] = 'first_name_first'
    if ('maxauthors' not in options):  options['maxauthors'] = 9
    if ('minauthors' not in options):  options['minauthors'] = 9
    if ('maxeditors' not in options):  options['maxeditors'] = 5
    if ('mineditors' not in options):  options['mineditors'] = 5
    if ('etal_message' not in options):  options['etal_message'] = '\\textit{et al.}'
    if ('use_name_ties' not in options):  options['use_name_ties'] = False
    if ('terse_inits' not in options):  options['terse_inits'] = False
    if ('french_intials' not in options):  options['french_intials'] = False
    if ('period_after_initial' not in options):  options['period_after_initial'] = True

    lastname = namedict['last']
    firstname = '' if ('first' not in namedict) else namedict['first']
    middlename = '' if ('middle' not in namedict) else namedict['middle']
    prefix = '' if ('prefix' not in namedict) else namedict['prefix']
    suffix = '' if ('suffix' not in namedict) else namedict['suffix']

    if options['use_firstname_initials']:
        if firstname:
            firstname = initialize_name(firstname, options) + '.'
        middlename = initialize_name(middlename, options)

    if middlename:
        if options['terse_inits']:
            frontname = firstname + middlename
            frontname.replace(' ','')
        elif options['use_name_ties']:
            middlename = middlename.replace(' ','~')    ## replace spaces with tildes
            frontname = firstname + '~' + middlename
        else:
            frontname = firstname + ' ' + middlename + '.'
    else:
        frontname = firstname

    ## Reconstruct the name string in the desired order for the formatted bibliography.
    if (options['namelist_format'] == 'first_name_first'):
        if (prefix != ''): prefix = ' ' + prefix
        if (suffix != ''): suffix = ', ' + suffix
        if (frontname + prefix != ''): prefix = prefix + ' '    ## provide a space before last name
        namestr = frontname + prefix + lastname + suffix
    elif (options['namelist_format'] == 'last_name_first'):
        if (prefix != ''): prefix = prefix + ' '
        if (suffix != ''): suffix = ', ' + suffix
        ## Provide a comma before the first name.
        if (frontname + suffix != ''): frontname = ', ' + frontname
        namestr = prefix + lastname + frontname + suffix

    return(namestr)

## =============================
def argsort(seq, reverse=False):
    '''
    Return the indices for producing a sorted list.

    Parameters
    ----------
    seq : iterable
        The iterable object to sort.
    reverse : bool
        Whether to return a reversed list.

    Returns
    -------
    idx : list of ints
        The indices needed for a sorted list.
    '''

    res = sorted(range(len(seq)), key=seq.__getitem__, cmp=locale.strcoll, reverse=reverse)
    return(res)

## =============================
def create_alphanum_citelabels(entrykey, bibdata, citelist):
    '''
    Create an alphanumeric style citation key (the first letter of the author's last name, followed by a number giving
    the sort order).

    Warning: do *not* run this function on a large database of citations --- it is not optimized for that use and will
    take quite a while to complete.

    Parameters
    ----------
    entry : dict
        The bibliography entry.
    bibdata : dict
        The entire bibliography database.
    citelist : list of str
        The sorted list of citation keys.

    Returns
    -------
    citelabels : str
        The dictionary of citation labels.
    '''

    citelabels = {}
    alphanums = []

    for c in citelist:
        if ('authorlist' in bibdata[c]):
            namelist = bibdata[c]['authorlist']
        elif ('editorlist' in bibdata[c]):
            namelist = bibdata[c]['editorlist']
        else:
            continue

        ## Note: you need to run "purify" before extracting the name, because the first character might be a
        ## curly brace that purify can get rid of, or the "first letter" be something like "\AA" that ought to
        ## be extracted as a single unicode character.
        letter = purify_string(namelist[0]['last'])[0]
        if (letter+'1' not in alphanums):
            citelabels[c] = letter+'1'
            alphanums.append(letter+'1')
            #print('[%s]: %s' % (c, letter+'1'))
        else:
            q = 1
            while (letter+str(q) in alphanums):
                q += 1
            citelabels[c] = letter+str(q)
            alphanums.append(letter+str(q))
            #print('[%s]: %s' % (c, letter+str(q)))

    return(citelabels)

## =============================
def get_implicit_loop_data(templatestr):
    '''
    From a template containing an implicit loop ('...' notation), build a full-size template without an ellipsis.

    Right now, the code only allows one implicit loop in any given template.

    Parameters
    ----------
    templatestr : str
        The input template string (containing the implicit loop ellipsis notation).

    Returns
    -------
    loop_data : dict
        A dictionary containing all of the information needed to build a loop for a template.

    '''

    idx = templatestr.find('...')
    lhs = templatestr[:idx]
    rhs = templatestr[idx+3:]

    ## In the string to the left of the ellipsis, look for the template variable farthest to the right. Note that
    ## we can't just set "lhs_var = lhs_variables[-1]" because we need to know the *position* of the variable and
    ## not just the variable name. And if the name occurs more than once in the template, then we can't easily get
    ## the position from the name. Thus, we iterate through the string until we encounter the last match, and
    ## return that.
    match = re.search(r'<.*?>', lhs)
    if not match:
        msg = 'Warning 030a: the template string "' + templatestr + '" is malformed. It does not have a ' + \
              'template variable to the left of the ellipsis (implied loop).'
        bib_warning(msg)
        return(None)

    for i,match in enumerate(re.finditer(r'<.*?>', lhs)):
        if (i > 1):
            msg = 'Warning 030b: the template string "' + templatestr + '" is malformed. Only one variable is allowed ' + \
                  'but the template has more than one.'
            bib_warning(msg)
        lhs_span = match.span()
    lhs_var = match.group()

    ## Get the part of the template that goes before the implicit loop.
    before_loop_stuff = lhs[:lhs_span[0]]

    ## "get_variable_name_elements()" returns a dictionary with keys "index", "name", "prefix", and "suffix".
    lhs_var_dict = get_variable_name_elements(lhs_var[1:-1])

    ## Now that we have the info about the LHS variable, let's also find out the "glue" string that needs to be
    ## inserted between all of the loop elements.
    lhs_glue = lhs[lhs_span[1]:]

    ## In the string to the right of the ellipsis, look for the template variable farthest to the right.
    match = re.search(r'<.*?>', rhs)
    if not match:
        msg = 'Warning 030c: the template string "' + templatestr + '" is malformed. It does not have a ' + \
              'template variable to the right of the ellipsis (implied loop).'
        bib_warning(msg)
        return(None)

    rhs_span = match.span()
    rhs_var = match.group()
    rhs_var_dict = get_variable_name_elements(rhs_var[1:-1])

    if (rhs_var_dict['name'] != lhs_var_dict['name']) or (rhs_var_dict['prefix'] != lhs_var_dict['prefix']) or \
            (rhs_var_dict['suffix'] != lhs_var_dict['suffix']):
        msg = 'Warning 030d: the template string "' + templatestr + '" is malformed. The LHS variable "' + \
              lhs_var + '" is not the same as the RHS variable "' + rhs_var + '".'
        bib_warning(msg)

    ## Get the RHS "glue" element. If it has curly braces in it, then we differentiate the conditions between when
    ## the number of names is only two (then use only the stuff inside the curly braces) and more than two (then
    ## use all of the glue). In both cases, remove the first and last curly braces before applying the glue.
    rhs_glue = rhs[0:rhs_span[0]]
    if re.search(r'\{.*?\}', rhs_glue):
        glue_start = rhs_glue.find('{')
        glue_end = rhs_glue.rfind('}')
        last_glue_if_only_two = rhs_glue[glue_start+1:glue_end]
        last_glue = rhs_glue[:glue_start] + rhs_glue[glue_start+1:glue_end] + rhs_glue[glue_end+1:]
    else:
        last_glue_if_only_two = rhs_glue
        last_glue = rhs_glue

    ## Get the part of the template that goes after the implicit loop.
    after_loop_stuff = rhs[rhs_span[1]:]

    loop_data = {}
    loop_data['varname'] = lhs_var_dict['name']
    loop_data['start_index'] = lhs_var_dict['index']
    loop_data['end_index'] = rhs_var_dict['index']
    loop_data['glue'] = lhs_glue
    loop_data['var_prefix'] = lhs_var_dict['prefix']
    loop_data['var_suffix'] = lhs_var_dict['suffix']
    loop_data['last_glue'] = last_glue
    loop_data['last_glue_if_only_two'] = last_glue_if_only_two
    loop_data['before_loop_stuff'] = before_loop_stuff
    loop_data['after_loop_stuff'] = after_loop_stuff

    return(loop_data)

## ==================================================================================================

if (__name__ == '__main__'):
    print('sys.argv=', sys.argv)
    user_locale = None
    if (len(sys.argv) > 1):
        try:
            (opts, args) = getopt.getopt(sys.argv[1:], '', ['locale='])
        except getopt.GetoptError as err:
            ## Print help information and exit.
            print(err)              ## this will print something like "option -a not recognized"
            print('Bibulous can be called with')
            print('    bibulous.py myfile.aux --locale=mylocale')
            print('where "locale" is an optional variable.')
            sys.exit(2)

        for o,a in opts:
            if (o == '--locale'):
                uselocale = a
            else:
                assert False, "unhandled option"

        arg_auxfile = args[0]
        files = arg_auxfile
    else:
        ## Use the test example input.
        arg_bibfile = './test/test1.bib'
        arg_auxfile = './test/test1.aux'
        arg_bstfile = './test/test1.bst'
        files = [arg_bibfile, arg_auxfile, arg_bstfile]

    main_bibdata = Bibdata(files, uselocale=user_locale, debug=False)

    ## Check if the bibliography database and style template files exist. If they don't, then the user didn't specify
    ## them, and it's probably true that there is no bibliography requested. That is, Bibulous was called without any
    ## need.
    if main_bibdata.filedict and main_bibdata.citedict:
        main_bibdata.write_bblfile()
        print('Writing to BBL file = ' + main_bibdata.filedict['bbl'])
        #os.system('kwrite ' + main_bibdata.filedict['bbl'])
        print('DONE')

