#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# pylint: disable-msg=C0321
# See the LICENSE.rst file for licensing information.
'''
Bibulous is a drop-in replacement for BibTeX, with the primary advantage that the bibliography
template format is compact and *very* easy to modify.

The basic program flow is as follows:

1. Read the `.aux` file and get the names of the bibliography databases (`.bib` files),
   the style templates (.bst files) to use, and the entire set of citations.
2. Read in all of the bibliography database files into one long dictionary (`bibdata`),
   replacing any abbreviations with their full form. Cross-referenced data is *not* yet
   inserted at this point. That is delayed until the time of writing the BBL file in order
   to speed up parsing.
3. Read in the Bibulous style template file as a dictionary (`bstdict`).
4. Now that all the information is collected, go through each citation key, find the
   corresponding entry key in `bibdata`. From the entry type, select a template from `bstdict`
   and begin inserting the variables one-by-one into the template. If any data is missing,
   check for cross-references and use crossref data to fill in missing values.
'''

from __future__ import unicode_literals, print_function, division     ## for Python3 compatibility
import re
import os
import sys
import codecs       ## for importing UTF8-encoded files
import locale       ## for language internationalization and localization
import getopt       ## for getting command-line options
import traceback    ## for getting full traceback info in exceptions
from math import log10
import pdb          ## put "pdb.set_trace()" at any place you want to interact with pdb

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

__version__ = '1.0'
__all__ = ['sentence_case', 'stringsplit', 'finditer', 'namefield_to_namelist',
           'namedict_to_formatted_namestr', 'initialize_name', 'get_delim_levels',
           'get_quote_levels', 'splitat', 'multisplit', 'enwrap_nested_string',
           'enwrap_nested_quotes', 'purify_string', 'latex_to_utf8', 'parse_bst_template_str',
           'namestr_to_namedict', 'search_middlename_for_prefixes', 'create_edition_ordinal',
           'export_bibfile', 'parse_pagerange', 'parse_nameabbrev', 'make_sortkey_unique',
           'filter_script', 'str_is_integer', 'warn']


class Bibdata(object):
    '''
    Bibdata is a class to hold all data related to a bibliography database, a citation list, and a
    style template.

    To initialize the class, either call it with the filename of the ".aux" file containing the
    relevant file locations (for the ".bib" database files and the ".bst" template files) or simply
    call it with a list of all filenames to be used (".bib", ".bst" and ".aux"). The output file
    (the LaTeX-formatted bibliography) is assumed to have the same filename root as the ".aux"
    file, but with ".bbl" as its extension.

    Attributes
    ----------
    abbrevs : dict
        The list of abbreviations given in the bibliography database file(s). The dictionary keys \
        are the abbreviations, and the values are their full forms.
    bibdata : dict
        The database of bibliography entries and fields derived from parsing the bibliography \
        database file(s).
    bstdict : dict
        The style template for formatting the bibliography. The dictionary keys are the \
        entrytypes, with the dictionary values their string template.
    citedict : dict
        The dictionary of citation keys, and their corresponding numerical order of citation.
    debug : bool
        Whether to turn on debugging features.
    filedict : dict
        The ditionary of filenames associated with the bibliographic data. The dictionary consists \
        of keys `bib`, `bst`, `aux`, `tex`, and `bbl`. The first two are lists of filenames, while
        the others contain only a single filename.
    filename : str
        (For error messages and debugging) The name of the file currently being parsed.
    i : int
        (For error messages and debugging) The line of the file currently being parsed.
    options : dict
        The dictionary containing the various option settings from the style template (BST) files.
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
        Whether to cull the database so that only cited entries are parsed. Setting this to False \
        means that the entire BIB file database will be parsed. When True, the BIB file parser \
        will only parse those entries corresponding to keys in the citedict.

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
    generate_sortkey
    create_namelist
    format_namelist
    insert_crossref_data
    write_citeextract
    write_authorextract
    replace_abbrevs_with_full
    generate_bibitem_label
    get_bibfilenames

    Example
    -------
    bibdata = Bibdata('jobname.aux')
    bibdata.write_bblfile()
    '''

    def __init__(self, filename, disable=None, culldata=True, debug=False):
        self.debug = debug
        self.abbrevs = {'jan':'1', 'feb':'2', 'mar':'3', 'apr':'4', 'may':'5', 'jun':'6',
                        'jul':'7', 'aug':'8', 'sep':'9', 'oct':'10', 'nov':'11', 'dec':'12'}
        self.locale = locale.setlocale(locale.LC_ALL,'')    ## set the locale to the user's default
        self.bibdata = {'preamble':''}
        self.filedict = {}  ## the dictionary containing all of the files associated with the bibliography
        self.citedict = {}  ## the dictionary containing the original data from the AUX file
        self.citelist = []  ## the *sorted* list of citation keys
        self.bstdict = {}   ## the dictionary containing all information from template files
        self.user_script = ''       ## any user-written Python scripts go here
        self.user_variables = {}    ## any user-defined variables from the BST files
        self.culldata = culldata    ## whether to cull the database so that only cited entries are parsed
        self.searchkeys = []        ## when culling data, this is the list of keys to limit parsing to

        ## Temporary variables for use in error messages while parsing files.
        self.filename = ''                      ## the current filename (for error messages)
        self.i = 0                              ## counter for line in file (for error messages)

        ## On default initialization, we don't want to issue any warnings about "overwriting" the
        ## default options. So if no "default" keyword is given, then turn off warning #9.
        if (disable == None):
            self.disable = [9]
        else:
            self.disable = disable              ## the list of warning message numbers to disable

        ## Put in default options settings.
        self.options = {}
        self.options['use_abbrevs'] = True
        self.options['undefstr'] = '???'
        self.options['namelist_format'] = 'first_name_first'
        self.options['citation_sort'] = 'citenum'
        self.options['citation_label'] = 'citekey'
        self.options['maxauthors'] = 100
        self.options['maxeditors'] = 100
        self.options['minauthors'] = 5
        self.options['mineditors'] = 5
        self.options['procspie_as_journal'] = False
        self.options['use_firstname_initials'] = True
        self.options['use_name_ties'] = False
        self.options['show_urls'] = False
        #self.options['backrefstyle'] = 'none'
        #self.options['backrefs'] = False
        self.options['sort_case'] = True
        self.options['french_initials'] = False
        self.options['sort_with_prefix'] = False
        self.options['period_after_initial'] = True
        self.options['terse_inits'] = False
        self.options['force_sentence_case'] = False
        self.options['bibitemsep'] = None
        self.options['month_abbrev'] = True
        self.options['allow_scripts'] = False
        self.options['case_sensitive_field_names'] = False

        ## Compile some patterns for use in regex searches.
        self.anybrace_pattern = re.compile(r'(?<!\\)[{}]', re.UNICODE)
        self.startbrace_pattern = re.compile(r'(?<!\\){', re.UNICODE)
        self.endbrace_pattern = re.compile(r'(?<!\\)}', re.UNICODE)
        self.quote_pattern = re.compile(r'(?<!\\)"', re.UNICODE)
        self.abbrevkey_pattern = re.compile(r'(?<!\\)[,#]', re.UNICODE)
        self.anybraceorquote_pattern = re.compile(r'(?<!\\)[{}"]', re.UNICODE)
        self.integer_pattern = re.compile(r'^-?[0-9]+', re.UNICODE)

        ## Get the list of filenames associated with the bibliography (AUX, BBL, BIB, TEX).
        ## Additionally, if the input "filename" contains only the AUX file, then we assume
        ## that the user wants only to parse that part if the database corresponding to the
        ## citation keys in the AUX file. This default behavior can be overriden (so that the
        ## entire database is parsed) is the optional keyword "cull_database" is set to False.
        self.get_bibfilenames(filename)

        ## Print out some info on Bibulous and the files it is working on.
        print('This is Bibulous, version ' + unicode(__version__))
        print('The current working directory is: ' + os.getcwd())
        print('The top-level TeX file: ' + unicode(self.filedict['tex']))
        print('The top-level auxiliary file: ' + unicode(self.filedict['aux']))
        print('The bibliography database file(s): ' + unicode(self.filedict['bib']))
        print('The Bibulous style template file(s): ' + unicode(self.filedict['bst']))
        print('The output formatted bibliography file: ' + unicode(self.filedict['bbl']))

        if self.filedict['aux']:
            self.parse_auxfile(self.filedict['aux'])

        if self.culldata:
            self.searchkeys = self.citedict.keys()

        #zzz
        print('SEARCHKEYS=', self.searchkeys)

        ## Parsing the style file has to go *before* parsing the BIB file, so that any style options
        ## that affect the way the data is parsed can take effect.
        if self.filedict['bst']:
            for f in self.filedict['bst']:
                self.parse_bstfile(f)

        if self.filedict['bib']:
            for f in self.filedict['bib']:
                self.parse_bibfile(f)

        if self.culldata:
            ## When culldata==True, things here get more complicated. The problem is that if a crossref
            ## refers to an entry that was not among the citation keys, then the database parser will
            ## not know to place that entry into the bibdata dictionary. Thus, if we happen to run
            ## across an entry with missing data, and it has a crossref that is not in the databse,
            ## then we have to go back and parse the database a second time, this time adding the
            ## crossreferenced items. Once that's done, *then* we can add cross-referenced data into
            ## the original cited entries.
            crossref_list = []
            for key in self.bibdata:
                if ('crossref' in self.bibdata[key]):
                    crossref_list.append(self.bibdata[key]['crossref'])
            if crossref_list:
                self.searchkeys = crossref_list

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

        self.filename = filename
        #filehandle = open(os.path.normpath(self.filename), 'rU')
        filehandle = codecs.open(os.path.normpath(self.filename), 'r', 'utf-8')

        ## This next block parses the lines in the file into a dictionary. The tricky part here is
        ## that the BibTeX format allows for multiline entries. So we have to look for places where
        ## a line does not end in a comma, and check the following line to see if it a continuation
        ## of that line. Unfortunately, this means we need to read the whole file into memory ---
        ## not just one line at a time.
        entry_brace_level = 0

        ## The variable "entrystr" contains all of the contents of the entry between the entrytype
        ## definition "@____{" and the closing brace "}". Once we've obtained all of the (in general
        ## multiline) contents, then we hand them off to parse_bibentry() to format them.
        entrystr = ''
        entrytype = None
        self.i = 0           ## line number counter --- for error messages only

        for line in filehandle:
            self.i += 1

            ## Ignore empty and comment lines.
            if not line: continue
            if line.strip().startswith('%'): continue
            if line.startswith('}'):
                ## If a line *starts* with a closing brace, then assume the intent is to close the
                ## current entry.
                entry_brace_level = 0
                self.parse_bibentry(entrystr, entrytype)       ## close out the entry
                entrystr = ''
                if (line[1:].strip() != ''):
                    warn('Warning 001a: line#' + unicode(self.i) + ' of "' + self.filename + '" has '
                          'data outside of an entry {...} block. Skipping all contents until the '
                          'next entry ...', self.disable)
                    #raise ValueError
                continue

            ## Don't strip off leading and ending whitespace until after checking if '}' begins a
            ## line (as in the block above).
            line = line.strip()

            if line.startswith('@'):
                brace_idx = line.find('{')             ## assume a form like "@ENTRYTYPE{"
                if (brace_idx == -1):
                    warn('Warning 002a: open brace not found for the entry beginning on line#' + \
                         unicode(self.i) + ' of "' + self.filename + '". Skipping to next entry ...',
                         self.disable)
                    entry_brace_level = 0
                    continue
                entrytype = line[1:brace_idx].lower().strip()   ## extract string between "@" and "{"
                line = line[brace_idx+1:]
                entry_brace_level = 1

            ## If we are not current inside an active entry, then skip the line and wait until the
            ## the next entry.
            if (entry_brace_level == 0):
                if (line.strip() != ''):
                    warn('Warning 001b: line#' + unicode(self.i) + ' of "' + self.filename + \
                         '" has data outside of an entry {...} block. Skipping all contents ' + \
                         'until the next entry ...', self.disable)
                    #raise ValueError
                continue

            ## Look if the entry ends with this line. If so, append it to "entrystr" and call the
            ## entry parser. If not, then simply append to the string and continue.
            endpos = len(line)

            for match in re.finditer(self.anybrace_pattern, line):
                if (match.group(0)[-1] == '}'):
                    entry_brace_level -= 1
                elif (match.group(0)[-1] == '{'):
                    entry_brace_level += 1
                if (entry_brace_level == 0):
                    ## If we've found the final brace, then check if there is anything after it.
                    if (line[match.end():].strip() != ''):
                        warn('Warning 002b: line#' + unicode(self.i) + ' of "' + self.filename + \
                             '" has data outside of an entry {...} block. Skipping all ' + \
                             'contents until the next entry ...', self.disable)
                        #raise ValueError
                    endpos = match.end()
                    break

            if (entry_brace_level == 0):
                entrystr += line[:endpos-1]         ## use "-1" to remove the final closing brace
                self.parse_bibentry(entrystr, entrytype)
                entrystr = ''
            else:
                entrystr += line[:endpos] + '\n'

        filehandle.close()
        return

    ## =============================
    def parse_bibentry(self, entrystr, entrytype):
        '''
        Given a string representing the entire contents of the BibTeX-format bibliography entry,
        parse the contents and place them into the bibliography preamble string, the set of
        abbreviations, and the bibliography database dictionary.

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
            ## In order to use the same "parse_bibfield()" function as all the other options, add a
            ## fake key onto the front of the string before calling "parse_bibfield()".
            fd = self.parse_bibfield('fakekey = ' + entrystr)
            if fd: self.bibdata['preamble'] += '\n' + fd['fakekey']
        elif (entrytype == 'string'):
            fd = self.parse_bibfield(entrystr)
            if fd: self.abbrevs.update(fd)
        elif (entrytype == 'acronym'):
            fd = self.parse_bibfield(entrystr)
            entrykey = fd.keys()[0]
            newentry = {'name':entrykey, 'description':fd[entrykey], 'entrytype':'acronym'}
            if fd: self.bibdata[entrykey] = newentry
        else:
            ## First get the entry key. Then send the remainder of the entry string to the parser.
            idx = entrystr.find(',')
            if (idx == -1):
                warn('Warning 003: the entry ending on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" is does not have an "," for defining the entry key. '
                     'Skipping ...', self.disable)
                return(fd)

            ## Get the entry key. If we are culling the database and the entry key is not among the
            ## citation keys, then exit --- we don't need to add this to the database.
            entrykey = entrystr[:idx].strip()
            if self.searchkeys and (entrykey not in self.searchkeys): return
            entrystr = entrystr[idx+1:]

            if not entrykey:
                warn('Warning 004a: the entry ending on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" has an empty key. Ignoring and continuing ...', self.disable)
                return
            elif (entrykey in self.bibdata):
                warn('Warning 004b: the entry ending on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" has the same key ("' + entrykey + '") as a previous ' + \
                     'entry. Overwriting the entry and continuing ...', self.disable)

            self.bibdata[entrykey] = {}
            self.bibdata[entrykey]['entrytype'] = entrytype
            fd = self.parse_bibfield(entrystr)
            if fd: self.bibdata[entrykey].update(fd)

        return

    ## =============================
    def parse_bibfield(self, entrystr):
        '''
        For a given string representing the raw contents of a BibTeX-format bibliography entry,
        parse the contents into a dictionary of key:value pairs corresponding to the field
        names and field values.

        Parameters
        ----------
        entrystr : str
            The string containing the entire contents of the bibliography entry.

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
                warn('Warning 005: the entry ending on line #' + unicode(self.i) + ' of file "' + \
                     self.filename + '" is an abbreviation-type entry but does not have an "=" '
                     'for defining the end of the abbreviation key. Skipping ...', self.disable)
                #raise ValueError
                return(fd)

            fieldkey = entrystr[:idx].strip()
            fieldstr = entrystr[idx+1:].strip()

            if not self.options['case_sensitive_field_names']:
                fieldkey = fieldkey.lower()

            if not fieldstr:
                entrystr = ''
                continue

            ## Next we go through the field contents, which may involve concatenating. When we
            ## reach the end of an individual field, we return the "result string" and
            ## truncate the entry string to remove the part we just finished parsing.
            resultstr = ''
            while fieldstr:
                firstchar = fieldstr[0]

                if (firstchar == ','):
                    ## Reached the end of the field, truncate the entry string return to the outer
                    ## loop over fields.
                    fd[fieldkey] = resultstr
                    entrystr = fieldstr[1:].strip()
                    break
                elif (firstchar == '#'):
                    ## Reached a concatenation operator. Just skip it.
                    fieldstr = fieldstr[1:].strip()
                elif (firstchar == '"'):
                    ## Search for the content string that resolves the double-quote delimiter.
                    ## Once you've found the end delimiter, append the content string to the
                    ## result string.
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
                    ## Search for the endbrace that resolves the brace level. Once you've found it,
                    ## add the intervening contents to the result string.
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
                    ## If the fieldstr doesn't begin with '"' or '{' or '#', then the next set of
                    ## characters must be an abbreviation key. An abbrev key ends with a whitespace
                    ## followed by either '#' or ',' (or the end of the field). Anything else is a
                    ## syntax error.
                    endpos = len(fieldstr)
                    end_of_field = False

                    ## The "abbrevkey_pattern" searches for the first '#' or ',' that is not
                    ## preceded by a backslash. If this pattern is found, then we've found the
                    ## *end* of the abbreviation key.
                    if not re.search(self.abbrevkey_pattern, fieldstr):
                        ## If the "abbrevkey" is an integer, then it's not actually an abbreviation.
                        ## Convert it to a string and insert the number itself.
                        abbrevkey = fieldstr
                        if re.match(self.integer_pattern, abbrevkey):
                            resultstr += unicode(abbrevkey)
                        else:
                            if abbrevkey in self.abbrevs:
                                resultstr += self.abbrevs[abbrevkey].strip()
                            else:
                                warn('Warning 006: for the entry ending on line #' + \
                                     unicode(self.i) + ' of file "' + self.filename + \
                                     '", cannot find the abbreviation key "' + abbrevkey + \
                                     '". Skipping ...', self.disable)
                                resultstr = self.options['undefstr']
                        fieldstr = ''
                        end_of_field = True
                    else:
                        (fieldstr, resultstr, end_of_field) = self.replace_abbrevs_with_full(fieldstr, resultstr)

                    ## Since we found the comma at the end of this field's contents, we break here
                    ## to return to the loop over fields.
                    if end_of_field:
                        entrystr = fieldstr.strip()
                        break

            ## Strip off any unnecessary white space and remove any newlines.
            resultstr = resultstr.strip().replace('\n',' ')

            ## Having braces around quotes can cause problems when parsing nested quotes, and
            ## do not provide any additional functionality.
            if ('{"}') in resultstr:
                resultstr = resultstr.replace('{"}', '"')
            if ("{'}") in resultstr:
                resultstr = resultstr.replace("{'}", "'")
            if ('{`}') in resultstr:
                resultstr = resultstr.replace('{`}', '`')

            fd[fieldkey] = resultstr

        return(fd)

    ## =============================
    def parse_auxfile(self, filename, debug=False):
        '''
        Read in an `.aux` file and convert the `\citation{}` entries found there into a dictionary
        of citekeys and citation order number.

        Parameters
        ----------
        filename : str
            The filename of the `.aux` file to parse.
        '''

        if debug: print('Reading AUX file "' + filename + '" ...')
        self.filename = filename
        #filehandle = open(os.path.normpath(self.filename), 'rU')
        filehandle = codecs.open(os.path.normpath(filename), 'r', 'utf-8')

        ## First go through the file and grab the list of citation keys. Once we get them all, then
        ## we can go through the list and figure out the numbering.
        keylist = []
        for line in filehandle:
            line = line.strip()
            if not line.startswith(r'\citation{'): continue

            ## Remove the "\citeation{" from the front and the "}" from the back. If multiple
            ## citations are given, then split them using the comma.
            items = line[10:-1].split(',')
            for item in items:
                keylist.append(item)
        filehandle.close()

        ## If you didn't find any citations in the file, issue a warning. Otherwise, build a
        ## dictionary of keys giving the citation keys with values equal to the citation order
        ## number.
        if not keylist:
            warn('Warning 007: no citations found in AUX file "' + filename + '"', self.disable)
        else:
            q = 1                       ## citation order counter
            self.citedict[keylist[0]] = q
            for key in keylist[1:]:
                if key in self.citedict: continue
                q += 1
                self.citedict[key] = q

        if debug:
            ## When displaying the dictionary, show it in order-sorted form. Remember to use
            ## the user's locale for the sort.
            for key in sorted(self.citedict, key=self.citedict.get, cmp=locale.strcoll):
                print(key + ': ' + unicode(self.citedict[key]))

        return

    ## =============================
    def parse_bstfile(self, filename):
        '''
        Convert a Bibulous-type bibliography style template into a dictionary.

        The resulting dictionary consists of keys which are the various entrytypes, and values which \
        are the template strings. In addition, any formatting options are stored in the "options" key \
        as a dictionary of option_name:option_value pairs.

        Parameters
        ----------
        filename : str
            The filename of the Bibulous style template to use.
        '''

        self.filename = filename
        #filehandle = open(os.path.normpath(filename), 'rU')
        filehandle = codecs.open(os.path.normpath(filename), 'r', 'utf-8')

        ## For the "definition_pattern", rather than matching the initial string up to the first
        ## whitespace character, we match a whitespace-equals-whitespace
        definition_pattern = re.compile(r'\s=\s', re.UNICODE)
        section = 'TEMPLATES'
        continuation = False    ## whether the current line is a continuation of the previous
        abort_script = False    ## if an unsafe object is being used, abort the user_script eval

        for i,line in enumerate(filehandle):
            ## Ignore any comment lines, and remove any comments from data lines.
            if line.startswith('#'): continue
            if ('#' in line):
                idx = line.index('#')
                line = line[:idx]
                if not line.strip(): continue       ## if the line contained only a comment

            if ('EXECUTE {' in line) or ('EXECUTE{' in line) or ('FUNCTION {' in line):
                raise ImportError('The style template file "' + filename + '" appears to be BibTeX '
                                  'format, not Bibulous. Aborting...')

            if line.strip().startswith('TEMPLATES:'):
                section = 'TEMPLATES'
                continuation = line.endswith('...')
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
                    warn('Warning 026a: Python script line #' + str(i) + ' of file "' + filename + \
                         '" contains an invalid use of "__".\nAborting script evaluation ...',
                         self.disable)
                    abort_script = True
                if re.search(r'\sos.\S', line, re.UNICODE):
                    warn('Warning 026b: Python script line #' + str(i) + ' of file "' + filename + \
                         '" contains an invalid call to the "os" module.\n' + \
                         'Aborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'\ssys.\S', line, re.UNICODE):
                    warn('Warning 026c: Python script line #' + str(i) + ' of file "' + filename + \
                         '" contains an invalid call to the "sys" module.\n' + \
                         'Aborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'\scodecs.\S', line, re.UNICODE):
                    warn('Warning 026c: Python script line #' + str(i) + ' of file "' + filename + \
                         '" contains an invalid call to the "codecs" module.\n' + \
                         'Aborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'^import\s', line, re.UNICODE):
                    warn('Warning 026d: Python script line #' + str(i) + ' of file "' + filename + \
                         '" contains an invalid call to "import".\n' + \
                         'Aborting script evaluation ...', self.disable)
                    abort_script = True
                if re.search(r'^import\s', line, re.UNICODE):
                    warn('Warning 026e: Python script line #' + str(i) + ' of file "' + filename + \
                         '" contains an invalid call to the "open()" function.\n' + \
                         'Aborting script evaluation ...', self.disable)
                    abort_script = True

                self.user_script += line
                if self.debug: print('Adding a line to the BST scripting string: ' + line, end='')

            line = line.strip()

            if (section == 'VARIABLES'):
                if not line: continue
                matchobj = re.search(definition_pattern, line)
                if (matchobj == None):
                    warn('Warning 008a: line #' + str(i) + ' of file "' + filename + '" does ' + \
                         'not contain a valid variable definition.\n Skipping ...', self.disable)
                    continue
                (start,end) = matchobj.span()
                var = line[:start].strip()
                value = line[end:].strip()
                self.user_variables[var] = filter_script(value)
                if self.debug:
                    print('Adding user variable "' + var + '" with value "' + value + '" ...')
            elif (section in ('TEMPLATES','OPTIONS')):
                ## Skip empty lines. It is tempting to put this line above here, but resist the
                ## temptation -- putting it higher above would remove empty lines from the Python
                ## scripts in the DEFINITIONS section, which would make troubleshooting those
                ## more difficult.
                if not line: continue
                if not continuation:
                    ## If the line ends with an ellpsis, then remove the ellipsis and set
                    ## continuation to True.
                    if line.endswith('...'):
                        line = line[:-3].strip()
                        continuation = True

                    matchobj = re.search(definition_pattern, line)
                    if (matchobj == None):
                        warn('Warning 008b: line #' + str(i) + ' of file "' + filename + '" does ' + \
                             'not contain a valid variable definition.\n Skipping ...', self.disable)
                        continue

                    (start,end) = matchobj.span()
                    var = line[:start].strip()
                    value = line[end:].strip()
                else:
                    ## If the line ends with an ellpsis, then remove the ellipsis and set
                    ## continuation to True.
                    if line.endswith('...'):
                        line = line[:-3].strip()
                        continuation = True
                    else:
                        continuation = False

                    value += line.strip()

                if (section == 'TEMPLATES'):
                    ## The line defines an entrytype template. Check whether this definition is
                    ## overwriting an already existing definition.
                    if (var in self.bstdict) and (self.bstdict[var] != value):
                        warn('Warning 009a: overwriting the existing template variable "' + var + \
                             '" from [' + self.bstdict[var] + '] to [' + value + '] ...',
                             self.disable)
                    self.bstdict[var] = value
                    if self.debug:
                        print('Setting BST variable "' + var + '" to value "' + value + '"')

                elif (section == 'OPTIONS'):
                    ## The variable defines an option rather than an entrytype. Check whether this definition is
                    ## overwriting an already existing definition.
                    if (var in self.options) and (str(self.options[var]) != value):\
                        warn('Warning 009b: overwriting the existing template option "' + var + \
                             '" from [' + unicode(self.options[var]) + '] to [' + \
                             unicode(value) + '] ...', self.disable)
                    ## If the value is numeric or bool, then convert the datatype from string.
                    if self.debug:
                        print('Setting BST option "' + var + '" to value "' + value + '"')

                    if value.isdigit():
                        value = int(value)
                    elif (value in ('True','False')):
                        value = (value == 'True')
                    self.options[var] = value

        filehandle.close()

        if abort_script:
            self.user_script = ''

        ## The "terse_inits" options has to override the "period_after_initial" option.
        if ('terse_inits' in self.options) and  self.options['terse_inits']:
            self.options['period_after_initial'] = False

        ## Next check to see whether any of the template definitions are simply maps to one
        ## of the other definitions. For example, one BST file may have a line of the form
        ##      inbook = incollection
        ## which implies that the template for "inbook" should be mapped to the same template
        ## as defined for the "incollection" entrytype.
        for key in self.bstdict:
            nwords = len(re.findall(r'\w+', self.bstdict[key]))
            if (nwords == 1) and ('<' not in self.bstdict[key]):
                self.bstdict[key] = self.bstdict[self.bstdict[key]]

        ## If the user defined any functions, then we want to evaluate them in a way such that
        ## they are available in other functions.
        if self.user_script and self.options['allow_scripts']:
            if self.debug:
                print('Evaluating the user script:\n' + 'v'*50 + '\n' + self.user_script + '^'*50 + '\n')
            exec(self.user_script, globals())

        if self.debug:
            ## When displaying the bst dictionary, show it in sorted form.
            for key in sorted(self.bstdict, key=self.bstdict.get, cmp=locale.strcoll):
                print('entrytype.' + key + ': ' + unicode(self.bstdict[key]))
            for key in sorted(self.options, key=self.options.get):
                print('options.' + key + ': ' + unicode(self.options[key]))

        return

    ## =============================
    def write_bblfile(self, filename=None, write_preamble=True, write_postamble=True, bibsize=None,
                      verbose=False):
        '''
        Given a bibliography database `bibdata`, a dictionary containing the citations called out \
        `citedict`, and a bibliography style template `bstdict` write the LaTeX-format file for the \
        formatted bibliography.

        Start with the preamble and then loop over the citations one by one, formatting each entry \
        one at a time, and put `\end{thebibliography}` at the end when done.

        Parameters
        ----------
        filename : str, optional
            The filename of the ".bbl" file to write. (Default is to take the AUX file and change \
            its extension to ".bbl".)
        write_preamble : bool, optional
            Whether to write the preamble. (Setting this to False can be useful when writing the \
            bibliography in separate steps, as in the testing suite.)
        write_postamble : bool, optional
            Whether to write the postamble. (Setting this to False can be useful when writing the \
            bibliography in separate steps, as in the testing suite.)
        bibsize : str, optional
            A string the length of which is used to determine the label margin for the bibliography.
        '''

        if (filename == None):
            filename = self.filedict['bbl']
        if not self.bstdict:
            raise ImportError('Not template file was found. Aborting writing the BBL file ...')
        if not self.citedict:
            raise ImportError('Not AUX file was found. Aborting writing the BBL file ...')

        if not write_preamble:
            filehandle = open(filename, 'a')
        else:
            filehandle = open(filename, 'w')

        ## Create an inverse dictionary for the month names. The month names are determined by the
        ## user's default locale.
        monthname_dict = {}
        for i in range(1,13):
            if self.options['month_abbrev']:
                ## The abbreviated form (i.e. 'jan').
                monthname_dict[unicode(i)] = locale.nl_langinfo(locale.__dict__['ABMON_'+unicode(i)]).title()
            else:
                ## The full form (i.e. 'january').
                monthname_dict[unicode(i)] = locale.nl_langinfo(locale.__dict__['MON_'+unicode(i)]).title()

        if write_preamble:
            if not bibsize: bibsize = repr(len(self.citedict))
            filehandle.write('\\begin{thebibliography}{' + bibsize + '}\n'.encode('utf-8'))
            #if self.options['show_urls']: filehandle.write(r'\providecommand{\url}[1]{\texttt{#1}}')
            #if not self.options['show_urls']:
            #    filehandle.write(r'\providecommand{\url}[1]{}')              ## i.e. ignore the URL
            filehandle.write("\\providecommand{\\enquote}[1]{``#1''}\n".encode('utf-8'))
            filehandle.write('\\providecommand{\\url}[1]{\\verb|#1|}\n'.encode('utf-8'))
            filehandle.write('\\providecommand{\\href}[2]{#2}\n'.encode('utf-8'))
            if (self.options['bibitemsep'] != None):
                s = '\\setlength{\\itemsep}{' + self.options['bibitemsep'] + '}\n'
                filehandle.write(s.encode('utf-8'))

            if ('preamble' in self.bibdata):
                filehandle.write(self.bibdata['preamble'].encode('utf-8'))

            filehandle.write('\n\n'.encode('utf-8'))

        ## Use a try-except block here, so that if any exception is raised then we can make sure to
        ## produce a valid BBL file.
        try:
            ## First Define a list which contains the citation keys, sorted in the order in which
            ## we need for writing into the BBL file.
            self.create_citation_list()

            ## Write out each individual bibliography entry. Some formatting options will actually
            ## cause the entry to be deleted, so we need the check below to see if the return
            ## string is empty before writing it to the file.
            for c in self.citelist:
                ## Verbose output is for debugging.
                if verbose: print('Writing entry "' + c + '" to "' + filename + '" ...')

                self.insert_crossref_data(c)
                self.create_namelist(c, 'author')
                self.create_namelist(c, 'editor')

                ## Before inserting entries into the BBL file, we do "difficult" BIB parsing jobs
                ## here: insert cross-reference data, format author and editor name lists, generate
                ## the "edition_ordinal", etc. Doing it here means that we don't have to add lots
                ## of extra checks later, allowing for simpler code.
                if (c in self.bibdata):
                    entry = self.bibdata[c]

                    if ('edition' in entry):
                        entry['edition_ordinal'] = create_edition_ordinal(entry,
                                                            disable=self.disable)

                    if ('pages' in entry):
                        (startpage,endpage) = parse_pagerange(entry['pages'], c, self.disable)
                        entry['startpage'] = startpage
                        entry['endpage'] = endpage

                    ## The "month" is stored in the bibdata dictionary as a string representing an
                    ## integer from 1 to 12. Here we need to translate it to a string name.
                    if ('month' in entry):
                        if entry['month'].isdigit():
                            monthname = monthname_dict[entry['month']]
                        else:
                            monthname = entry['month']
                        entry['monthname'] = monthname

                    if ('doi' in entry):
                        if not entry['doi'].startswith('http://dx.doi.org/'):
                            entry['doi'] = 'http://dx.doi.org/' + entry['doi']

                ## Now that we have generated all of the "special" fields, we can call the bibitem
                ## formatter to generate the output for this entry.
                s = self.format_bibitem(c)
                if (s != ''):
                    ## Need two line EOL's here and not one so that backrefs can work properly.
                    filehandle.write((s + '\n').encode('utf-8'))
        except:
            if write_postamble:
                filehandle.write('\n\\end{thebibliography}\n'.encode('utf-8'))
            filehandle.close()
            raise           ## re-raise the exception

        if write_postamble:
            filehandle.write('\n\\end{thebibliography}\n'.encode('utf-8'))
        filehandle.close()
        return


    ## ===================================
    def create_citation_list(self):
        '''
        Create the list of citation keys, sorted into the proper order.
        '''

        ## Create a temporary dictionary to hold the citation keys (as dictionary values) and the
        ## strings we wish to use for sorting (as the dictionary keys).
        sortdict = {}

        ## Generate a sortkey for each citation. If the sortkey is already present in the
        ## dictionary, it will replace the the old entry with the new, and we would lose a citation
        ## in the process. To prevent this, we need to make sure that it is unique.
        for c in self.citedict:
            sortkey = self.generate_sortkey(c)
            if (sortkey in sortdict):
                sortkey = make_sortkey_unique(sortkey, sortdict)
            sortdict[sortkey] = unicode(c)      ## use "unicode()" to convert to string in case the key is an integer

        ## This part can be a little tricky. If the sortkey is generated such that it begins with an
        ## integer, then we should make sure that negative-values get sorted in front of positive
        ## ones. This happens in simple sort() but not when we use locale's "strcoll". So we have to
        ## separate the two cases manually. Also, use [::-1] on the negative integers because they
        ## need to be ordered from largest number to smallest.
        if (self.options['citation_sort'][0] == 'y'):
            firstdict = {k:sortdict[k] for k in sortdict if k[0] == '-'}
            seconddict = {k:sortdict[k] for k in sortdict if k[0] != '-'}
            self.citelist = sorted(firstdict.iterkeys(), cmp=locale.strcoll)[::-1]
            self.citelist += sorted(seconddict.iterkeys(), cmp=locale.strcoll)
        else:
            self.citelist = sorted(sortdict.iterkeys(), cmp=locale.strcoll)

        ## If using a citation order which is descending rather than ascending, then reverse the list.
        if (self.options['citation_sort'] == 'ydnt'):
            self.citelist = self.citelist[::-1]

        ## Finally, now that we have them in the order we want, we keep only the citation keys, so
        ## that we know which entry maps to which in the ".aux" file.
        self.citelist = [sortdict[a] for a in self.citelist]
        for c in self.citelist:
            sortkey = (key for key,value in sortdict.items() if value==c).next()
            if self.debug:
                print('citekey=%20s: sortkey=%s' % (c, sortkey))

        return

    ## =============================
    def format_bibitem(self, citekey, debug=False):
        '''
        Create the "\bibitem{...}" string to insert into the ".bbl" file.

        This is the workhorse function of Bibulous. For a given citation key, find the resulting
        entry in the bibliography database. From the entry's `entrytype`, lookup the relevant
        template in bstdict and start replacing template variables with formatted elements of the
        database entry. Once you've replaced all template variables, you're done formatting that
        entry. Write the result to the BBL file.

        Parameters
        ----------
        citekey : str
            The citation key.

        Returns
        -------
        itemstr : str
            The string containing the \bibitem{} citation key and LaTeX-formatted string for the
            formatted bibliography. (That is, this string is designed to be inserted directly into
            the LaTeX document.)
        '''

        c = citekey
        if (c == 'preamble'):
            return('')

        ## Although "citenum" or "citenumber" is really the only appropriate name for this sorting
        ## order, we also provide "none", "plain", "unsrt", and "abbrv" for users used to the other
        ## BibTeX names.
        numeric_tag_styles = ('citenumber', 'citenum', 'none', 'unsrt', 'plain', 'abbrv')
        if (self.options['citation_label'] in numeric_tag_styles):
            itemstr = r'\bibitem{' + c + '}\n'
        else:
            bibitem_label = self.generate_bibitem_label(c)
            itemstr = r'\bibitem[' + bibitem_label + ']{' + c + '}\n'

        ## If the citation key is not in the database, replace the format string with a message to the
        ## fact.
        if (c not in self.bibdata):
            msg = 'citation key "' + c + '" is not in the bibliography database.'
            warn('Warning 010: ' + msg, self.disable)
            return(itemstr + '\\textit{Warning: ' + msg + '}.')
        else:
            entry = self.bibdata[c]

        entrytype = entry['entrytype']

        if debug:
            print('Formatting entry "' + citekey + '"')
            print('Template: "' + self.bstdict[entrytype] + '"')
            print('Field data: ' + repr(entry))

        ## If the journal format uses ProcSPIE like a journal, then you need to change the entrytype
        ## from "inproceedings" to "article", and add a "journal" field.
        if self.options['procspie_as_journal'] and (entrytype == 'inproceedings') and \
            ('series' in entry) and (entry['series'] in ['Proc. SPIE','procspie']):
            entrytype = 'article'
            entry['entrytype'] = 'article'
            entry['journal'] = 'Proc. SPIE'

        if (entrytype in self.bstdict):
            templatestr = self.bstdict[entrytype]
        else:
            msg = 'entrytype "' + entrytype + '" does not have a template defined ' + \
                  'in the .bst file'
            warn('Warning 011: ' + msg, self.disable)
            return(itemstr + '\\textit{Warning: ' + msg + '}.')

        ## Process the optional arguments. First check the syntax. Make sure that there are the same
        ## number of open as closed brackets.
        num_obrackets = templatestr.count('[')
        num_cbrackets = templatestr.count(']')
        if (num_obrackets != num_cbrackets):
            msg = 'In the template for entrytype "' + entrytype + '" there are ' + \
                  unicode(num_obrackets) + ' open brackets "[", but ' + unicode(num_cbrackets) + \
                  ' close brackets "]" in the formatting string.'
            warn('Warning 012: ' + msg, self.disable)
            return(itemstr + '\\testit{' + msg + '}.')

        ## Get the list of all the variables used by the template string.
        variables = re.findall(r'<.*?>', templatestr)

        ## Before checking which variables are defined and which not, we first need to evaluate the
        ## user-defined variables or else they will always be "undefined". To make this work, we
        ## also need to provide the user shortcut names:
        if self.user_variables and self.options['allow_scripts']:
            options = self.options
            citedict = self.citedict
            bstdict = self.bstdict
            bibdata = self.bibdata
            for user_var_name in self.user_variables:
                user_var_value = eval(self.user_variables[user_var_name])
                self.bibdata[c][user_var_name] = user_var_value

        ## Next go through the template and replace each variable with the appropriate string from
        ## the database. Start with the three special cases. This block of code has to go before
        ## the "parse_bst_template_str()" call below to ensure that these variables are defined
        ## when they are evaluated there.
        if ('<authorliststr>' in templatestr) and ('authorlist' in entry):
            entry['authorliststr'] = self.format_namelist(entry['authorlist'], 'author')
        if ('<editorliststr>' in templatestr) and ('editorlist' in entry):
            entry['editorliststr'] = self.format_namelist(entry['editorlist'], 'editor')

        ## Next, do a nested search. From the beginning of the formatting string look for the first
        ## '[', and the first ']'. If they are out of order, raise an exception. Note that this
        ## assumes that the square brackets cannot be nested. (Is there something important which
        ## would require that functionality?)
        for i in range(num_obrackets):
            start_idx = templatestr.index('[')
            end_idx = templatestr.index(']')
            if not (start_idx < end_idx):
                msg = 'A closed bracket "]" occurs before an open bracket "[" in the format ' + \
                      'string "' + templatestr + '".'
                warn('Warning 013: ' + msg, self.disable)
                return(itemstr + '\\testit{' + msg + '}.')

            ## Remove the outer square brackets, and use the resulting substring as an input to the
            ## parser.
            substr = templatestr[start_idx+1:end_idx]

            ## In each options train, go through and replace the whole train with the one block that
            ## has a defined value.
            res = parse_bst_template_str(substr, entry, variables, undefstr=self.options['undefstr'])
            templatestr = templatestr[:start_idx] + res + templatestr[end_idx+1:]

        if ('<title>' in templatestr) and ('title' in entry):
            if self.options['force_sentence_case']:
                title = sentence_case(entry['title'])
            else:
                title = entry['title']

            ## If the template string has punctuation right after the title, and the title itself
            ## also has punctuation, then you may get something like "Title?," where the two
            ## punctuation marks conflict. In that case, keep the title's punctuation and drop the
            ## template's.
            if title.endswith(('?','!')):
                idx = templatestr.index('<title>')
                if (templatestr[idx + len('<title>')] in (',','.','!','?',';',':')):
                    templatestr = templatestr[:idx+len('<title>')] + templatestr[idx+1+len('<title>'):]
                    templatestr = templatestr.replace('<title>', title)
            else:
                templatestr = templatestr.replace('<title>', title)

        ## Remove the special cases from the variables list --- we already replaced these above.
        ## (Right now there is only <title> here, but we can add more.)
        specials_list = ('<title>')
        variables = [item for item in variables if item not in specials_list]

        for var in variables:
            if (var in templatestr):
                varname = var[1:-1]     ## remove angle brackets to extract just the name
                ## Check if the variable is defined and that it is not None (or empty string).
                if (varname in entry) and entry[varname]:
                    templatestr = templatestr.replace(var, unicode(entry[varname]))
                elif (varname in self.user_variables) and self.options['allow_scripts']:
                    user_var_value = eval(self.user_variables[varname])

                    if user_var_value:
                        templatestr = templatestr.replace(var, unicode(user_var_value))
                    else:
                        templatestr = templatestr.replace(var, self.options['undefstr'])
                else:
                    templatestr = templatestr.replace(var, self.options['undefstr'])

        ## Add the template string onto the "\bibitem{...}\n" line in front of it.
        itemstr = itemstr + templatestr

        ## Now that we've replaced template variables, go ahead and replace the special commands.
        if (r'{\makeopenbracket}' in itemstr):
            itemstr = itemstr.replace(r'{\makeopenbracket}', '[')
        if (r'{\makeclosebracket}' in itemstr):
            itemstr = itemstr.replace(r'{\makeclosebracket}', ']')
        if (r'{\makeverticalbar}' in itemstr):
            itemstr = itemstr.replace(r'{\makeverticalbar}', '|')
        if (r'{\makegreaterthan}' in itemstr):
            itemstr = itemstr.replace(r'{\makegreaterthan}', '>')
        if (r'{\makelessthan}' in itemstr):
            itemstr = itemstr.replace(r'{\makelessthan}', '<')

        ## If there are nested operators on the string, replace all even-level operators with \{}.
        ## Is there any need to do this with \textbf{} and \texttt{} as well?
        if (itemstr.count('\\textit{') > 1):
            itemstr = enwrap_nested_string(itemstr, delims=('{','}'), odd_operator=r'\textit', \
                                           even_operator=r'\textup')
        if (itemstr.count('\\textbf{') > 1):
            itemstr = enwrap_nested_string(itemstr, delims=('{','}'), odd_operator=r'\textbf', \
                                           even_operator=r'\textmd')

        ## If there are any nested quotation marks in the string, then we need to modify the
        ## formatting properly. If there are any apostrophes or foreign words that use apostrophes
        ## in the string then the current code will raise an exception.
        itemstr = enwrap_nested_quotes(itemstr, disable=self.disable)

        return(itemstr)

    ## ===================================
    def generate_sortkey(self, citekey):
        '''
        From a bibliography entry and the formatting template options, generate a sorting key for the
        entry.

        Parameters
        ----------
        citekey : str
            The key for the current entry.

        Returns
        -------
        sortkey : str
            A string to use as a sorting key.
        '''

        ## When a given citation key is not found in the database, return a warning. However, if the
        ## citeorder if just "citekey" then we *already* know how to sort it, so rather than return a
        ## warning go ahead and return the citekey so that it gets sorted properly. The fact that the
        ## key is not in the database will raise an error later.
        citeorder = self.options['citation_sort']
        if (citeorder == 'citekey'):
            return(citekey)

        if citekey not in self.bibdata:
            msg = '"' + citekey + '" is not in the bibliography database.'
            warn('Warning 014: ' + msg, self.disable)
            return('Warning: ' + msg)

        ## If we are ordering by the order of appearance of the citations in the text, then the key
        ## is most likely an integer type rather than a string, which causes problems. We can
        ## use "unicode()" to convert the int-type to string, but this won't sort properly --- "10"
        ## will get sorted between "1" and "2". So we need to pad with zeros. How many zeros depends
        ## on how many citations there are.
        if (citeorder in ('citenum','citenumber')):
            ncites = len(self.citedict)
            ndigits = 1 + int(log10(ncites))
            sortkey = unicode(self.citedict[citekey]).zfill(ndigits)
            return(sortkey)

        ## If the citation order used is "citenum", then any sortkey field in the entry is ignored.
        bibentry = self.bibdata[citekey]
        if ('sortkey' in bibentry):
            return(bibentry['sortkey'])

        namelist = []

        ## Use the name abbreviation (if it exists) in the sortkey.
        if ('sortname' in bibentry) and ('nameabbrev' in bibentry['sortname']):
            nameabbrev_dict = parse_nameabbrev(bibentry['sortname']['nameabbrev'])
        elif ('nameabbrev' in bibentry):
            nameabbrev_dict = parse_nameabbrev(bibentry['nameabbrev'])
        else:
            nameabbrev_dict = None

        ## Extract the last name of the first author.
        if ('sortname' in bibentry):
            namelist = namefield_to_namelist(bibentry['sortname'], key=citekey,
                                             nameabbrev=nameabbrev_dict, disable=self.disable)
            name = namelist[0]['last']
            if ('first' in namelist[0]): name += namelist[0]['first']
            if ('middle' in namelist[0]): name += namelist[0]['middle']
        else:
            if ('author' in bibentry):
                self.create_namelist(citekey, 'author')
                namelist = self.bibdata[citekey]['authorlist']
                name = namelist[0]['last']
                if self.options['sort_with_prefix'] and ('prefix' in namelist[0]):
                    name = namelist[0]['prefix'] + name
                if ('first' in namelist[0]): name += namelist[0]['first']
                if ('middle' in namelist[0]): name += namelist[0]['middle']
            elif ('editor' in bibentry):
                self.create_namelist(citekey, 'editor')
                namelist = self.bibdata[citekey]['editorlist']
                name = namelist[0]['last']
                if self.options['sort_with_prefix'] and ('prefix' in namelist[0]):
                    name = namelist[0]['prefix'] + name
                if ('first' in namelist[0]): name += namelist[0]['first']
                if ('middle' in namelist[0]): name += namelist[0]['middle']
            elif ('organization' in bibentry):
                name = bibentry['organization']
            elif ('institution' in bibentry):
                name = bibentry['institution']
            else:
                name = ''

        ## Names that have initials will have unwanted '.'s in them.
        name = name.replace('.','')

        ## To make sure that alphabetical sorting treats numbers correctly, we need to append zeros
        ## so that, say, "10" does not get sorted before "2". Note that this formatting should work
        ## for years between -999 and +9999.
        if ('sortyear' in bibentry):
            if str_is_integer(bibentry['sortyear']):
                year = unicode('%04i' % int(bibentry['sortyear']))
            else:
                year = bibentry['sortyear']
        elif ('year' in bibentry):
            if str_is_integer(bibentry['year']):
                year = unicode('%04i' % int(bibentry['year']))
            else:
                year = bibentry['year']
        else:
            year = '9999'

        ## "presort" is a string appended to the beginning of each sortkey. This can be useful for
        ## grouping entries.
        presort = '' if ('presort' not in bibentry) else unicode(bibentry['presort'])

        ## "sorttitle" is an alternative title used for sorting. Can be useful if the title contains
        ## special characters and LaTeX commands.
        if ('sorttitle' in bibentry):
            title = bibentry['sorttitle']
        else:
            title = '' if ('title' not in bibentry) else bibentry['title']

        volume = '0' if ('volume' not in bibentry) else unicode(bibentry['volume'])

        ## The different formatting options for the citation order are "nty"/"plain", "nyt", "nyvt",
        ## "anyt", "anyvt", ynt", "ydnt", "tny".
        if (citeorder in ('nyt','plain')):
            sortkey = presort + name + year + title
        elif (citeorder == 'nty'):
            sortkey = presort + name + title + year
        elif (citeorder == 'nyvt'):
            sortkey = presort + name + year + volume + title
        elif (citeorder in ('ynt','ydnt')):
            sortkey = presort + year + name + title
        elif (citeorder == 'tny'):
            sortkey = presort + title + name + year
        elif (citeorder == 'alpha'):
            if (len(namelist) == 1):
                concat_name = name[0:3]
            elif (len(namelist) > 1):
                if namelist:
                    concat_name = ''
                    for name in namelist:
                        concat_name += name['last'].strip('{}')[0]
                    #concat_name = ''.join([name['last'].strip('{}')[0] for name in namelist])
                else:
                    concat_name = name[0:3]
            sortkey = presort + concat_name[0:3] + year[-2:]
        elif (citeorder == 'anyt'):
            alpha = '' if ('alphalabel' not in bibentry) else bibentry['alphalabel']
            sortkey = presort + alpha + name + year + title
        elif (citeorder == 'anyvt'):
            alpha = '' if ('alphalabel' not in bibentry) else bibentry['alphalabel']
            sortkey = presort + alpha + name + year + volume + title
        else:
            raise KeyError('That citation sort order ("' + citeorder + '") is not supported.')

        sortkey = purify_string(sortkey)

        if not self.options['sort_case']:
            sortkey = sortkey.lower()

        return(sortkey)

    ## =============================
    def create_namelist(self, key, nametype):
        '''
        Deconstruct the bibfile string following "author = ..." (or "editor = ..."), and create a
        new field `authorlist` or `editorlist` that is a list of dictionaries (one dict for each
        person).

        Parameters
        ----------
        key : str
            The key in `bibdata` defining the current entry being formatted.
        nametype : str, {'author','editor'}
            Which bibliography field to use for parsing names.
        '''

        ## First check that the entrykey exists.
        if (key not in self.bibdata):
            return

        ## If the name field does not exist, we can't define name dictionaries, so exit. Note that
        ## we need not check for cross-reference data, since we will assume that has already been
        ## done.
        if (nametype not in self.bibdata[key]):
            return

        ## If the namelist is already defined, then there is nothing to do!
        if (nametype+'list' in self.bibdata[key]):
            return

        ## The name abbreviations are assumed to be used for generating initials, and so skip
        ## using abbrevations when not initializing.
        if (self.options['use_firstname_initials']) and ('nameabbrev' in self.bibdata[key]):
            nameabbrev_dict = parse_nameabbrev(self.bibdata[key]['nameabbrev'])
        else:
            nameabbrev_dict = None

        ## Convert the raw string containing author/editor names in the BibTeX field into a list
        ## of dictionaries --- one dict for each person.
        namelist = namefield_to_namelist(self.bibdata[key][nametype], key=key,
                                         nameabbrev=nameabbrev_dict, disable=self.disable)
        self.bibdata[key][nametype+'list'] = namelist

        return

    ## =============================
    def format_namelist(self, namelist, nametype):
        '''
        Format a list of dictionaries (one dict for each person) into a long string, with the
        format according to the directives in the bibliography style template.

        Parameters
        ----------
        namelist : str
            The list of dictionaries containing all of the names to be formatted.
        nametype : str, {'author', 'editor'}
            Whether the names are for authors or editors.

        Returns
        -------
        namestr : str
            The formatted form of the "name string". This is generally a list of authors or list \
            of editors.
        '''

        use_first_inits = self.options['use_firstname_initials']
        namelist_format = self.options['namelist_format']

        ## First get all of the options variables needed below, depending on whether the function is
        ## operating on a list of authors or a list of editors. Second, insert "authorlist" into the
        ## bibliography database entry so that other functions can have access to it. (This is the
        ## "author" or "editor" string parsed into individual names, so that each person's name is
        ## represented by a dictionary, and the whole set of names is a list of dicts.)
        if (nametype == 'author'):
            maxnames = self.options['maxauthors']
            minnames = self.options['minauthors']
        elif (nametype == 'editor'):
            maxnames = self.options['maxeditors']
            minnames = self.options['mineditors']

        ## This next block generates the list "namelist", which is a list of strings, with each
        ## element of `namelist` being a single author's name. That single author's name is encoded
        ## as a dictionary with keys "first", "middle", "prefix", "last", and "suffix".
        npersons = len(namelist)
        new_namelist = []
        for person in namelist:
            ## The BibTeX standard states that a final author in the authors field of "and others"
            ## should be taken as meaning to use \textit{et al.} at the end of the author list.
            if ('others' in person['last']) and ('first' not in person):
                npersons -= 1
                maxnames = npersons - 1
                continue

            ## From the person's name dictionary, create a string of the name in the format
            ## desired for the final BBL file.
            formatted_name = namedict_to_formatted_namestr(person, options=self.options,
                                                           use_firstname_initials=use_first_inits,
                                                           namelist_format=namelist_format)
            new_namelist.append(formatted_name)

        ## Now that we have the complete list of pre-formatted names, we need to join them together
        ## into a single string that can be inserted into the template.
        if (npersons == 1):
            namestr = new_namelist[0]
        elif (npersons == 2):
            namestr = ' and '.join(new_namelist)
        elif (npersons > 2) and (npersons <= maxnames):
            ## Make a string in which each person's name is separated by a comma, except the last name,
            ## which has a comma then "and" before the name.
            namestr = ', '.join(new_namelist[:-1]) + ', and ' + new_namelist[-1]
        elif (npersons > maxnames):
            ## If the number of names in the list exceeds the maximum, then truncate the list to the
            ## first "minnames" only, and add "et al." to the end of the string giving all the names.
            namestr = ', '.join(new_namelist[:minnames]) + r', \textit{et al.}'
        else:
            raise ValueError('How did you get here?')

        ## Add a tag onto the end if describing an editorlist.
        if (nametype == 'editor'):
            if (npersons == 1):
                namestr += ', ed.'
            else:
                namestr += ', eds'

        return(namestr)

    ## =============================
    def insert_crossref_data(self, entrykey, fieldname=None):
        '''
        Insert crossref info into a bibliography database dictionary.

        Loop through a bibliography database dictionary and, for each entry which has a "crossref"
        field, locate the crossref entry and insert any missing bibliographic information into the
        main entry's fields.

        Parameters
        ----------
        entrykey : str
            The key of the bibliography entry to query.
        fieldname : str, optional
            The name of the field to check. If fieldname==None, then check all fields.

        Returns
        -------
        foundit : bool
            Whether the function found a crossref for the queried field. If multiple fieldnames \
            were input, then foundit will be True if a crossref is located for any one of them.
        '''

        ## First check that the entrykey exists.
        if (entrykey not in self.bibdata):
            return

        bibentry = self.bibdata[entrykey]
        if ('crossref' not in self.bibdata[entrykey]):
            return

        if (fieldname == None):
            fieldnames = bibentry.keys()
        else:
            if isinstance(fieldname, list):
                fieldnames = fieldname
            else:
                fieldnames = [fieldname]

        for field in fieldnames:
            if (field not in bibentry):
                continue

            ## Check that the crossreferenced entry actually exists. If not, then just move on.
            if (self.bibdata[entrykey]['crossref'] in self.bibdata):
                crossref_keys = self.bibdata[self.bibdata[entrykey]['crossref']]
            else:
                warn('Warning 015: bad cross reference. Entry "' + entrykey + '" refers to ' + \
                     'entry "' + self.bibdata[entrykey]['crossref'] + '", which doesn\'t exist.',
                     self.disable)
                continue

            for k in crossref_keys:
                if (k not in self.bibdata[entrykey]):
                    self.bibdata[entrykey][k] = self.bibdata[self.bibdata[entrykey]['crossref']][k]

            ## What a "booktitle" is in the entry is normally a "title" in the crossref.
            if ('title' in crossref_keys) and ('booktitle' not in self.bibdata[entrykey]):
                self.bibdata[entrykey]['booktitle'] = self.bibdata[self.bibdata[entrykey]['crossref']]['title']

        return

    ## =============================
    def write_citeextract(self, outputfile, debug=False):
        '''
        Extract a sub-database from a large bibliography database, with the former containing only \
        those entries cited in the .aux file.

        Parameters
        ----------
        filedict :  str
            The dictionary filenames must have keys "aux",  "bst", and "bib".
        outputfile : str, optional
            The filename to use for writing the extracted BIB file.
        '''

        ## A dict comprehension to extract only the relevant items in "bibdata".
        bibextract = {c: self.bibdata[c] for c in self.citedict}
        export_bibfile(bibextract, outputfile)
        return

    ## =============================
    def write_authorextract(self, searchname, outputfile=None, debug=False):
        '''
        Extract a sub-database from a large bibliography database, with the former containing only \
        those entries citing the given author/editor.

        Parameters
        ----------
        searchname : str or dict
            The string or dictionary for the author's name. This can be, for example, "Bugs E. Bunny"
            or {'first':'Bugs', 'last':'Bunny', 'middle':'E'}.
        outputfile : str, optional
            The filename of the extracted BIB file to write.
        '''

        if not isinstance(searchname, basestring):
            raise TypeError('The input search name ["' + unicode(searchname) + \
                            '"] is not a valid string.')
        if not outputfile:
            outputfile = self.filedict['aux'][:-4] + '_authorextract.bib'

        searchname = namestr_to_namedict(searchname, self.disable)
        nkeys = len(searchname.keys())

        ## Find out if any of the tokens in the search name are initials. If so, then we need to
        ## perform the search over initialized names and not full names. Save the set of booleans
        ## (one for each name part) in a dictionary to use in the search loop below.
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
                self.create_namelist(k, 'author')
                name_list_of_dicts = self.bibdata[k]['authorlist']
            if ('editor' in self.bibdata[k]):
                self.create_namelist(k, 'editor')
                if not ('author' in self.bibdata[k]):
                    name_list_of_dicts = self.bibdata[k]['editorlist']
                else:
                    ## If the entry has both authors and editors, then just merge the two name
                    ## lists.
                    name_list_of_dicts += self.bibdata[k]['editorlist']

            if not name_list_of_dicts:
                continue

            ## Compare each name dictionary in the entry with the input author's name dict.
            ## All of an author's name keys must equal an entry's name key to produce a match.
            for name in name_list_of_dicts:
                if (searchname['last'] not in name['last']): continue

                key_matches = 0
                for namekey in name:
                    if (namekey in searchname):
                        if name_is_initialized[namekey]:
                            thisname = initialize_name(name[namekey])
                        else:
                            thisname = name[namekey]

                        if (thisname == searchname[namekey]):
                            key_matches += 1
                            if debug: print('Found match in entry "' + k + '": name[' + namekey + '] = ' + name[namekey])

                if (key_matches == nkeys):
                    #print(k, bibdata[k]['author'])
                    bibextract[k] = self.bibdata[k]
                    nentries += 1
                    if debug: print('Match FULL NAME in entry "' + k + '": ' + repr(name))

        export_bibfile(bibextract, outputfile)

        return

    ## =============================
    def replace_abbrevs_with_full(self, fieldstr, resultstr):
        '''
        Given an input str, locate the abbreviation key within it and replace the abbreviation with
        its full form.

        Once the abbreviation key is found, remove it from the "fieldstr" and add the full form to
        the "resultstr".

        Parameters
        ==========
        fieldstr : str
            The string to search for the abbrevation key.
        resultstr : str
            The thing to hold the abbreviation's full form. (Note that it might not be empty on \
            input.)

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

        ## The "abbrevkey_pattern" seaerches for the first '#' or ',' that is not preceded by a
        ## backslash. If this pattern is found, then we've found the *end* of the abbreviation key.
        for match in re.finditer(self.abbrevkey_pattern, fieldstr):
            endpos = match.end()
            if (match.group(0)[0] == '#'):
                abbrevkey = fieldstr[:endpos-1].strip()
                ## If the "abbreviation" is an integer, then it's not an abbreviation
                ## but rather a number, and just return it as-is.
                if abbrevkey.isdigit() or not self.options['use_abbrevs']:
                    resultstr += unicode(abbrevkey)
                elif (abbrevkey not in self.abbrevs):
                    warn('Warning 016a: for the entry ending on line #' + unicode(self.i) + \
                         ' of file "' + self.filename + '", cannot find the '
                         'abbreviation key "' + abbrevkey + '". Skipping ...', self.disable)
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
                    warn('Warning 016b: for the entry ending on line #' + unicode(self.i) + \
                         ' of file "' + self.filename + '", cannot find the '
                         'abbreviation key "' + abbrevkey + '". Skipping ...', self.disable)
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
    def generate_bibitem_label(self, citekey):
        '''
        Generate the bibitem label.

        Parameters
        ----------
        citekey : str
            The citation key.

        Returns
        -------
        bibitem_label : str
            The label to use for the reference list item.
        '''

        labelstyle = self.options['citation_label']
        if not (citekey in self.bibdata):
            warn('Warning 028: cannot find citation key "' + citekey + '" in the database. '
                 'Ignoring and continuing ...', self.disable)
            return(citekey)

        entry = self.bibdata[citekey]

        if ('name' in labelstyle):
            if ('author' in entry):
                name = purify_string(entry['authorlist'][0]['last'])
            elif ('editor' in entry):
                name = purify_string(entry['editorlist'][0]['last'])
            elif ('name' in entry):
                name = purify_string(entry['name'])
            else:
                name = self.options['undefstr']

        if ('year' in labelstyle):
            if ('year' in entry) and str_is_integer(entry['year']):
                year = entry['year']
            else:
                year = self.options['undefstr']

        if (labelstyle == 'name'):
            bibitem_label = name
        elif (labelstyle == 'name-year'):
            bibitem_label = name + '-' + year
        elif (labelstyle == 'name, year'):
            bibitem_label = name + ', ' + year
        elif (labelstyle == 'name (year)'):
            bibitem_label = name + ' (' + year + ')'
        elif (labelstyle == 'citekey'):
            bibitem_label = citekey
        elif (labelstyle == 'alpha'):
            if ('author' in entry):
                namelist = entry['authorlist']
            elif ('editor' in entry):
                namelist = entry['editorlist']

            if (len(namelist) == 1):
                name = purify_string(namelist[0]['last'])[0:3]
            elif (len(namelist) == 2):
                name = purify_string(namelist[0]['last'])[0]
                name += purify_string(namelist[1]['last'])[0]
            elif (len(namelist) > 2):
                name = purify_string(namelist[0]['last'])[0]
                name += purify_string(namelist[1]['last'])[0]
                name += purify_string(namelist[2]['last'])[0]

            if ('year' in entry) and str_is_integer(entry['year']):
                year = entry['year'][-2:]
            else:
                year = self.options['undefstr'][0:2]

            bibitem_label = name + year
        else:
            warn('Warning 027: The reference list label style "' + labelstyle + '" is not ' + \
                 'implemented ...', self.disable)
            bibitem_label = 'Unknown-' + self.options['undefstr']

        return(bibitem_label)


    ## =============================
    def write_auxfile(self, filename=None):
        '''
        Given the input database file(s) and style file(s), write out an AUX file containing
        citations to all unique database entries.

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
        If the input is a filename ending in '.aux', then read through the .aux file and locate the
        lines `\bibdata{...}` and `\bibstyle{...}` to get the filename(s) for the bibliography database
        and style template.

        Also determine whether to set the "culldata" flag. If the input is a single AUX filename,
        then the default is to set culldata=True. If the input is a list of filenames, then assume
        that this is the complete list of files to use (i.e. ignore the contents of the AUX file
        except for generating the citedict), and set culldata=False.

        Parameters
        ----------
        filename : str
            The "auxiliary" file, containing citation info, TOC info, etc.

        Returns
        -------
        filedict : dict
            A dictionary with keys 'bib' and 'bst', each entry of which contains a list of filenames.
        '''

        bibfiles = []
        bstfiles = []
        auxfile = ''
        bblfile = ''
        texfile = ''

        if isinstance(filename, basestring) and filename.endswith('.aux'):
            auxfile = os.path.normpath(os.path.abspath(filename))
            path = os.path.dirname(auxfile) + '/'

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

            ## Now we have the strings from the ".tex" file that describing the bibliography filenames.
            ## If these are lists of filenames, then split them out.
            if (',' in bibres):
                bibres = bibres.split(',')      ## if a list of files, then split up the list pieces
            else:
                bibres = [bibres]

            for r in bibres:
                ## If the filename is missing the extension, then add it.
                if not r.endswith('.bib'):
                    r += '.bib'

                ## If the filename has a relative address, convert it to an absolute one.
                ## Linux absolute paths begin with a forward slash
                ## Windows absolute paths begin with a drive letter and a colon.
                if not r.startswith('/') or (r[0].isalpha() and r[1] == ':'):
                    r = path + r
                elif r.startswith('./'):
                    r = path + r[2:]

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

                ## If the filename has a relative address, convert it to an absolute one.
                ## Linux absolute paths begin with a forward slash
                ## Windows absolute paths begin with a drive letter and a colon.
                if not r.startswith('/') or (r[0].isalpha() and r[1] == ':'):
                    r = path + r
                elif r.startswith('./'):
                    r = path + r[2:]

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
            ## All the work above was to locate the filenames from a single AUX file. However, if the
            ## input is a list of filenames, then constructing the filename dictionary is simple.
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

        ## Now that we have the filenames, build the dictionary of BibTeX-related files.
        self.filedict['bib'] = bibfiles
        self.filedict['bst'] = bstfiles
        self.filedict['tex'] = texfile
        self.filedict['aux'] = auxfile
        self.filedict['bbl'] = bblfile

        if self.debug:
            print('bib files: ' + repr(bibfiles))
            print('bst files: ' + repr(bstfiles))
            print('tex file: "' + unicode(texfile) + '"')
            print('aux file: "' + unicode(auxfile) + '"')
            print('bbl file: "' + unicode(bblfile) + '"')

        return()


## ================================================================================================
## END OF BIBDATA CLASS.
## ================================================================================================

## ===================================
def sentence_case(s):
    '''
    Reduce the case of the string to lower case, except for the first character in the string, and
    except if any given character is at nonzero brace level.

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

    ## Next we look for LaTeX commands, given by a backslash followed by a non-word character.
    ## Do not reduce those characters in the LaTeX command to lower case. To facilitate that, add
    ## one to the brace level for each of those character positions.
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
    Split a string into tokens, taking care not to allow the separator to act unless at brace
    level zero.

    Parameters
    ----------
    s : str
        The string to split.

    Returns
    -------
    tokens : list of str
        The list of tokens.
    '''

    ## The item separating the name tokens can be either a space character or a tilde, if the
    ## tilde is not preceded by a backslash (in which case it instead represents an accent
    ## character and not a separator).
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
                #print('n,j=', n, j)
                tokens.append(s[j:])
            else:
                nexti = indices[n+1][0]      ## the beginning of the *next* separator
                j = indices[n][1]            ## the end of *this* separator
                #print('n,j,nexti=', n, j, nexti)
                tokens.append(s[j:nexti])

    return(tokens)

## ===================================
def finditer(a_str, sub):
    '''
    A generator replacement for re.finditer() but without using regex expressions.

    Parameters
    ----------
    a_str : str
        The string to query.
    sub : str
        The substring to match to.

    Yields
    ------
    start : int
            The start index of the match
    '''

    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += 1

## =============================
def namefield_to_namelist(namefield, key=None, nameabbrev=None, disable=None):
    '''
    Parse a name field ("author" or "editor") of a BibTeX entry into a list of dicts, one for
    each person.

    Parameters
    ----------
    namefield : str
        Either the "author" field of a database entry or the "editor" field.
    key : str
        The bibliography data entry key.
    nameabbrev : dict
        The dictionary for translating names to their abbreviated forms.
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    namelist : list
        A list of dictionaries, with one dictionary for each name. Each dict has keys "first",
        "middle", "prefix", "last", and "suffix". The "last" key is the only one that is required.
    '''

    namefield = namefield.strip()
    namelist = []

    ## Look for common typos.
    if re.search('\sand,\s', namefield, re.UNICODE):
        warn('Warning 017a: The name string in entry "' + unicode(key) + '" has " and, ", which is '
             'likely a typo. Continuing on anyway ...', disable)
    if re.search(', and', namefield, re.UNICODE):
        warn('Warning 017b: The name string in entry "' + unicode(key) + '" has ", and", which is '
             'likely a typo. Continuing on anyway ...', disable)

    if (nameabbrev != None):
        for key in nameabbrev:
            if key in namefield: namefield = namefield.replace(key, nameabbrev[key])

    ## Split the string of names into individual strings, one for each complete name. Here we
    ## can split on whitespace surround the word "and" so that "{and}" and "word~and~word" will
    ## not allow the split. Need to treat the case of a single author separate from that of
    ## multiple authors in order to return a single-element *list* rather than a scalar.
    if not re.search('\sand\s', namefield, re.UNICODE):
        namedict = namestr_to_namedict(namefield, disable)
        namelist.append(namedict)
    else:
        if '{' not in namefield:
            names = re.split('\sand\s', namefield)
        else:
            ## If there are braces in the string, then we need to be careful to only allow
            ## splitting of the names when ' and ' is at brace level 0. This requires replacing
            ## re.split() with a bunch of low-level code.
            z = get_delim_levels(namefield, ('{','}'))
            separators = []

            for match in re.finditer(r'\sand\s', namefield):
                (i,j) = match.span()
                if (z[i] == 0):
                    ## Record the indices of the start and end of the match.
                    separators.append((i,j))

            num_names = len(separators)
            names = []
            if (num_names == 0):
                names.append(namefield)
            if (num_names > 0) and (separators[0][0] > 0):
                names.append(namefield[:separators[0][0]])

            ## Go through each match's indices and split the string at each.
            for n in xrange(num_names):
                if (n == num_names-1):
                    j = separators[n][1]            ## the end of *this* separator
                    #print('n,j=', n, j)
                    names.append(namefield[j:])
                else:
                    nexti = separators[n+1][0]      ## the beginning of the *next* separator
                    j = separators[n][1]            ## the end of *this* separator
                    #print('n,j,nexti=', n, j, nexti)
                    names.append(namefield[j:nexti])

        nauthors = len(names)
        for i in range(nauthors):
            namedict = namestr_to_namedict(names[i], disable)
            namelist.append(namedict)

    return(namelist)

## =============================
def namedict_to_formatted_namestr(namedict, options=None, use_firstname_initials=True,
                                  namelist_format='first_name_first', nameabbrev=None):
    '''
    Convert a name dictionary into a formatted name string.

    Parameters
    ----------
    namedict : dict
        The name dictionary (contains a required key "last" and optional keys "first", "middle", \
        "prefix", and "suffix".
    options : dict, optional
        Includes formatting options such as
        'use_name_ties': Whether to use '~' instead of spaces to tie together author initials.
        'terse_inits': Whether to format initialized author names like "RMA Azzam" instead of \
            the default form "R. M. A. Azzam".
        'french_intials': Whether to initialize digraphs with two letters instead of the default \
            of one. For example, if use_french_initials==True, then "Christian" -> "Ch.", not "C.".
        'period_after_initial': Whether to include a '.' after the author initial.
    use_firstname_initials : bool
        Whether or not to initialize first names.
    namelist_format : str
        The type of format to use for name formatting. ("first_name_first", "last_name_first")
    nameabbrev : list of str
        A list of names and their abbreviations.

    Returns
    -------
    namestr : str
        The formatted string of the name.
    '''

    if (options == None):
        options['use_name_ties'] = False
        options['terse_inits'] = False
        options['french_intials'] = False
        options['period_after_initial'] = True

    lastname = namedict['last']
    firstname = '' if ('first' not in namedict) else namedict['first']
    middlename = '' if ('middle' not in namedict) else namedict['middle']
    prefix = '' if ('prefix' not in namedict) else namedict['prefix']
    suffix = '' if ('suffix' not in namedict) else namedict['suffix']

    if use_firstname_initials:
        firstname = initialize_name(firstname, options)
        middlename = initialize_name(middlename, options)

    if (middlename != ''):
        if options['terse_inits']:
            frontname = firstname + middlename
            frontname.replace(' ','')
        elif options['use_name_ties']:
            middlename = middlename.replace(' ','~')    ## replace spaces with tildes
            frontname = firstname + '~' + middlename
        else:
            frontname = firstname + ' ' + middlename
    else:
        frontname = firstname

    ## Reconstruct the name string in the desired order for the formatted bibliography.
    if (namelist_format == 'first_name_first'):
        if (prefix != ''): prefix = ' ' + prefix
        if (suffix != ''): suffix = ', ' + suffix
        if (frontname + prefix != ''): prefix = prefix + ' '    ## provide a space before last name
        namestr = frontname + prefix + lastname + suffix
    elif (namelist_format == 'last_name_first'):
        if (prefix != ''): prefix = prefix + ' '
        if (suffix != ''): suffix = ', ' + suffix
        ## Provide a comma before the first name.
        if (frontname + suffix != ''): frontname = ', ' + frontname
        namestr = prefix + lastname + frontname + suffix

    return(namestr)

## ===================================
def initialize_name(name, options=None, debug=False):
    '''
    From an input name element (first, middle, prefix, last, or suffix) , convert it to its
    initials.

    Parameters
    ----------
    name : str
        The name element to be converted.
    options : dict, optional
        Includes formatting options such as
        'use_name_ties': Whether to use '~' instead of spaces to tie together author initials.
        'terse_inits': Whether to format initialized author names like "RMA Azzam" instead of \
            the default form "R. M. A. Azzam".
        'french_intials': Whether to initialize digraphs with two letters instead of the default \
            of one. For example, if use_french_initials==True, then "Christian" -> "Ch.", not "C.".
        'period_after_initial': Whether to include a '.' after the author initial.

    Returns
    -------
    new_name : str
        The name element converted to its initials form.
    '''

    if (name == ''):
        return(name)
    if (options == None):
        options = {}
        options['period_after_initial'] = True
        options['french_initials'] = False
        options['terse_inits'] = False

    ## Go through the author's name elements and truncate the first and middle names to their
    ## initials. If using French initials, then a hyphenated name produces hyphenated initials
    ## (for example "Jean-Paul" -> "J.-P." and not "J."), and a name beginning with a digraph
    ## produces a digraph initial, so that Philippe -> Ph. (not P.), and Christian -> Ch. (not C.).
    digraphs = ('Ch','Gn','Ll','Ph','Ss','Ch','Ph','Th')
    period = '.' if options['period_after_initial'] else ''

    ## Split the name by spaces (primarily used for middle name strings, which may have multiple
    ## names in them), and remove any empty list elements produced by the split.
    tokens = list(name.split(' '))
    tokens = [x for x in tokens if x]

    for j,nametoken in enumerate(tokens):
        if nametoken.startswith('{') and nametoken.endswith('}'): continue

        if ('-' in nametoken):
            ## If the name is hyphenated, then initialize the hyphenated parts of it, and assemble
            ## the result by combining initials with the hyphens. That is, "Chein-Ing" -> "C.-I.".
            pieces = nametoken.split('-')
            tokens[j] = '-'.join([initialize_name(p, options) for p in pieces])
        else:
            ## If the token already ends in a period then it's might already be an initial, but
            ## only if it has length 2. Otherwise you still need to truncate it.
            ## If the name only has one character in it, then treat it as a full name that doesn't
            ## need initializing.
            if nametoken.endswith('.') and (len(nametoken) == 2):
                tokens[j] = nametoken[0] + period
            elif (len(nametoken) > 1):
                if options['french_initials'] and (nametoken[:2] in digraphs):
                    tokens[j] = nametoken[:2] + period
                else:
                    tokens[j] = nametoken[0] + period
            else:
                tokens[j] = nametoken

    if options['terse_inits']:
        newname = ''.join(tokens).replace(period,'')
    else:
        newname = ' '.join(tokens)

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
    ldelim : str
        The left-hand-side delimiter.
    rdelim : str
        The right-hand-side delimiter.
    is_regex : bool
        Whether the delimiters are expressed as regular expressions or as simple strings.

    Returns
    -------
    oplevels : list of ints
        A list giving the operator delimiter level (or "brace level" if no operator is given) of \
        each character in the string.
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
    '''
    q = 0   ## counter for the character ending a line
    if ('\n' in s):
        for line in s.split('\n'):
            print(line)
            print(unicode(levels[q:q+len(line)])[2:-1].replace(',','').replace(' ',''))
            q += len(line)
    else:
        print(s)
        print(unicode(levels)[2:-1].replace(',','').replace(' ',''))
    return

## ===================================
def get_quote_levels(s, disable=None, debug=False):
    '''
    Return a list which gives the "quotation level" of each character in the string.

    Parameters
    ----------
    s : str
        The string to analyze.
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    alevels : list
        The double-quote-level for (``,'') pairs in the string.
    blevels : list
        The single-quote-level for (`,') pairs in the string.
    clevels : list
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
                ## The trouble with single-quotes is the clash with apostrophes. So, only increment
                ## the single-quote counter if we think it is the start of a quote (not immediately
                ## preceded by a non-whitespace character).
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
        warn('Warning 018a: found mismatched "``"..."''" quote pairs in the input string "' + s + \
             '". Ignoring the problem and continuing on ...', disable)
        alevels[-1] = 0
    if (blevels[-1] > 0):
        warn('Warning 018b: found mismatched "`"..."\'" quote pairs in the input string "' + s + \
             '". Ignoring the problem and continuing on ...', disable)
        blevels[-1] = 0
    if (clevels[-1] > 0):
        warn('Warning 018c: found mismatched '"'...'"' quote pairs in the input string "' + s + \
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

    This can be used more flexibly than Python's native string split() function, when the character
    you are splitting on is not always a valid splitting location.

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
            #print(n, start, end)
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
    This function will return the input string if it finds there
    are no nested operators inside (i.e. when the number of delimiters found is < 2).

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
        warn('Warning 019: found mismatched "{","}" brace pairs in the input string. '
             'Ignoring the problem and continuing on ...', disable)
        return(s)

    ## In the operator queue, we replace all even-numbered levels while leaving all odd-numbered
    ## levels alone. Recall that "oplevels" encodes the position of the *delimiter* and not the
    ## position of where the operator starts.
    maxlevels = max(oplevels)
    if (maxlevels < 2):
        return(s)

    ## Select only even levels starting at 2. "q" is a counter for the number of substr
    ## replacements.
    q = 0
    shift = len(odd_operator) - len(even_operator)
    for i,level in enumerate(oplevels):
        if (level > 0) and (level % 2 == 0):
            ## Any place we see a transition from one level lower to this level is a substr we want
            ## to replace. The "shift" used here is to compensate for changes in the length of the
            ## string due to differences in length between the input operator and output.
            if (oplevels[i-1] < level):
                #print(i, level, oplevels[i-1], s, s[:i-len(odd_operator)], s[i:])
                s = s[:i-len(odd_operator)-(q*shift)] + even_operator + s[i-(q*shift):]
                q += 1

    return(s)

## ===================================
def enwrap_nested_quotes(s, disable=None, debug=False):
    '''
    Find nested quotes within strings and, if necessary, replace them with the proper nesting
    (i.e. outer quotes use ````...''`` while inner quotes use ```...'``).

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

    ## NOTE: There is quite a lot going on in this function, so it may help future development
    ## to write some of this work into subroutines.

    ## First check for cases where parsing is going to be very complicated. For now, we should just
    ## flag these cases to inform the user that they need to modify the source to tell the parser
    ## what they want to do.
    if ("```" in s) or ("'''" in s):
        warn('Warning 020: the input string ["' + s + '"] contains multiple unseparated quote '
             'characters. Bibulous cannot unnest the single and double quotes from this set, so '
             'the separate quotations must be physically separated like ``{\:}`, for example. '
             'Ignoring the quotation marks and continuing ...', disable)
        return(s)

    ## Note that a backtick preceded by a backslash, an explamation point, or a question mark,
    ## indicates LaTeX markup for a grave accent, an inverted explamation point, and an inverted
    ## question mark, respectively.
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

    ## First, we look at the quote stack and replace *all* quote pairs with \enquote{...}. When
    ## done, we can use `enwrap_nested_string()` to replace the odd and even instances of
    ## \enquote{} with different quotation markers, depending on locale. `q` is the amount of
    ## shift between indices in the current string and those in the source string.
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

    ## Finally, replace odd levels of quotation with "``" and even levels with "`".
    ## TODO: This approach is the American convention. Need to generalize this behavior for British
    ## convention, and, even more broadly, to all locale-dependent quotation mark behavior. For
    ## now let's just try to get the American version working.
    t = 0
    odd_operators = ("``","''")
    even_operators = ("`","'")

    if debug:
        show_levels_debug(s, qlevels)

    for i,level in enumerate(qlevels):
        if (qlevels[i-1] == 0) and (level == 0): continue

        ## Any place we see a transition from one level lower to this level is a substr we want
        ## to replace. The shift "t" used here is to compensate for changes in the length of the
        ## string due to differences in length between the input operator and output. Also,
        ## if we are about to substitute in a quote character (or two, in the case of LaTeX
        ## double quotes), then we need to be careful to look in front and see if the quotes butt
        ## up against one another, in which case we need to add a small space. For example, LaTeX
        ## will interpret ''' as a double ending quote followed by a single ending quote, even if
        ## we meant it to be the other way around. The space "\:" will remove the ambiguity.

        ## There is quite a lot going on in this loop, so it may help future work to replace some
        ## of the operations here with subroutines.
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
    Remove the LaTeX-based formatting elements from a string so that a sorting function can use \
    alphanumerical sorting on the string.

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

    ## If the string contains mathematical markup (i.e. $...$), then we have to treat that case
    ## specially, since we don't want to run "purify" on mathematics --- it's not as easy as
    ## simply replacing math markup with unicode equivalents. So, if we find math markup then
    ## we split the string into math parts and non-math parts, purify the non-math ones, and
    ## then piece it back together.
    mathpattern = re.compile(r'(?<!\\)\$.*?(?<!\\)\$', re.UNICODE)
    matchobj = re.search(r'(?<!\\)\$.*?(?<!\\)\$', s, re.UNICODE)

    if matchobj:
        start_idx = []
        end_idx = []

        for matchobj in re.finditer(r'(?<!\\)\$.*?(?<!\\)\$', s, re.UNICODE):
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

        ## Next we look for LaTeX commands. LaTeX variables will have the form "\variable" followed
        ## by either whitespace, '{', or '}'. A function will have the form "\functionname{...}"
        ## where the ellipsis can be anything.
        match = re.compile(r'\\\w+', re.UNICODE)
        p = match.sub('', p)

        ## Finally, remove the braces used for LaTeX commands. We can't just replace '{' and '}'
        ## wholesale, since the syntax allows '\{' and '\}' to produce text braces. So first we
        ## remove the command braces, and then we swap '\{' for '{' etc at the end.
        match = re.compile(r'(?<!\\){', re.UNICODE)
        p = match.sub('', p, re.UNICODE)
        match = re.compile(r'(?<!\\)}', re.UNICODE)
        p = match.sub('', p, re.UNICODE)
        p = p.replace('\\{', '{')
        p = p.replace('\\}', '}')

    return(p)

## =============================
## I think that we can get rid of the "u" in front of the strings now that we are using
## "from __future__ import unicode_literals".
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

    ## Note that the code below uses replace() loops rather than a translation table, since the
    ## latter only supports one-to-one translation, whereas something more flexible is needed
    ## here. There is a substantial
    if ('\\' not in s):
        return(s)

    ## First, some easy replacements.
    trans = {r'\$':'$', r'\%':'%', r'\_':'_', r'\&':'&', r'\#':'#', r'!`':'¡', r'?`':'¿'}
    for c in trans:
        if c in s: s = s.replace(c, trans[c])

    ## If there are any double backslashes, place some braces around them to prevent something like
    ## "\\aa" from getting interpreted as a backslash plus "\aa". This makes the string easier to
    ## parse and does no harm.
    if r'\\' in s:
        s = s.replace(r'\\',r'{\\}')

    ## First identify all the LaTeX special characters in the string, then replace them all with
    ## their Unicode equivalents. (This is to make sure that they alphabetize correctly for
    ## sorting.)
    ##     The translation dictionary below uses single-letter accent commands, such as \u{g}.
    ## These commands are one of (r'\b', r'\c', r'\d', r'\H', r'\k', r'\r', r'\u', r'\v'), followed
    ## by an open brace, a single character, and a closed brace. These replacements are done first
    ## because some of the special characters use '\i', which would otherwise get replaced by the
    ## "dotless i" Unicode character, and so the replacement dictionary here would not detect
    ## the proper LaTeX code for it.

    ## First, characters with a cedilla or comma below.
    if (r'\c' in s):
        trans = {r'\c{C}':'Ç', r'{\c C}':'Ç', r'\c{c}':'ç', r'{\c c}':'ç',
                 r'\c{E}':'Ȩ', r'{\c E}':'Ȩ', r'\c{e}':'ȩ', r'{\c e}':'ȩ',
                 r'\c{G}':'Ģ', r'{\c G}':'Ģ', r'\c{g}':'ģ', r'{\c g}':'ģ',
                 r'\c{K}':'Ķ', r'{\c K}':'Ķ', r'\c{k}':'ķ', r'{\c k}':'ķ',
                 r'\c{L}':'Ļ', r'{\c L}':'Ļ', r'\c{l}':'ļ', r'{\c l}':'ļ',
                 r'\c{N}':'Ņ', r'{\c N}':'Ņ', r'\c{n}':'ņ', r'{\c n}':'ņ',
                 r'\c{R}':'Ŗ', r'{\c R}':'Ŗ', r'\c{r}':'ŗ', r'{\c r}':'ŗ',
                 r'\c{S}':'Ş', r'{\c S}':'Ş', r'\c{s}':'ş', r'{\c s}':'ş',
                 r'\c{T}':'Ţ', r'{\c T}':'Ţ', r'\c{t}':'ţ', r'{\c t}':'ţ'}

        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Characters with breve above. Note that the "\u" is problematic when "unicode_literals" is
    ## turned on via "from __future__ import unicode_literals". Thus, in the block below, rather
    ## than raw strings with single backslashes, we have to use double-backslashes.
    if ('\\u' in s):
        trans = {'\\u{A}':'Ă', '{\\u A}':'Ă', '\\u{a}':'ă',  '{\\u a}':'ă',
                 '\\u{E}':'Ĕ', '{\\u E}':'Ĕ', '\\u{e}':'ĕ',  '{\\u e}':'ĕ',
                 '\\u{G}':'Ğ', '{\\u G}':'Ğ', '\\u{g}':'ğ',  '{\\u g}':'ğ',
                 '\\u{I}':'Ĭ', '{\\u I}':'Ĭ', '\\u{\i}':'ĭ', '{\\u\i}':'ĭ',
                 '\\u{O}':'Ŏ', '{\\u O}':'Ŏ', '\\u{o}':'ŏ',  '{\\u o}':'ŏ',
                 '\\u{U}':'Ŭ', '{\\u U}':'Ŭ', '\\u{u}':'ŭ',  '{\\u u}':'ŭ'}

        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Characters with an ogonek.
    if (r'\k' in s):
        trans = {r'\k{A}':'Ą', r'{\k A}':'Ą', r'\k{a}':'ą', r'{\k a}':'ą',
                 r'\k(E}':'Ę', r'{\k E}':'Ę', r'\k{e}':'ę', r'{\k e}':'ę',
                 r'\k{I}':'Į', r'{\k I}':'Į', r'\k{i}':'į', r'{\k i}':'į',
                 r'\k{O}':'Ǫ', r'{\k O}':'Ǫ', r'\k{o}':'ǫ', r'{\k o}':'ǫ',
                 r'\k{U}':'Ų', r'{\k U}':'Ų', r'\k{u}':'ų', r'{\k u}':'ų'}
        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Characters with hachek.
    if (r'\v' in s):
        trans = {r'\v{C}':'Č', r'{\v C}':'Č', r'\v{c}':'č', r'{\v c}':'č',
                 r'\v{D}':'Ď', r'{\v D}':'Ď', r'\v{d}':'ď', r'{\v d}':'ď',
                 r'\v{E}':'Ě', r'{\v E}':'Ě', r'\v{e}':'ě', r'{\v e}':'ě',
                 r'\v{L}':'Ľ', r'{\v L}':'Ľ', r'\v{l}':'ľ', r'{\v l}':'ľ',
                 r'\v{N}':'Ň', r'{\v N}':'Ň', r'\v{n}':'ň', r'{\v n}':'ň',
                 r'\v{R}':'Ř', r'{\v R}':'Ř', r'\v{r}':'ř', r'{\v r}':'ř',
                 r'\v{S}':'Š', r'{\v S}':'Š', r'\v{s}':'š', r'{\v s}':'š',
                 r'\v{T}':'Ť', r'{\v T}':'Ť', r'\v{t}':'ť', r'{\v t}':'ť',
                 r'\v{Z}':'Ž', r'{\v Z}':'Ž', r'\v{z}':'ž', r'{\v z}':'ž',
                 r'\v{H}':'\u021E', r'{\v H}':'\u021E', r'\v{h}':'\u021F', r'{\v h}':'\u021F',
                 r'\v{A}':'\u01CD', r'{\v A}':'\u01CD', r'\v{a}':'\u01CE', r'{\v a}':'\u01CE',
                 r'\v{I}':'\u01CF', r'{\v I}':'\u01CF', r'\v{\i}':'\u01D0', r'{\v \i}':'\u01D0',
                 r'\v{O}':'\u01D1', r'{\v O}':'\u01D1', r'\v{o}':'\u01D2', r'{\v o}':'\u01D2',
                 r'\v{U}':'\u01D3', r'{\v U}':'\u01D3', r'\v{u}':'\u01D4', r'{\v u}':'\u01D4',
                 r'\v{G}':'\u01E6', r'{\v G}':'\u01E6', r'\v{g}':'\u01E7', r'{\v g}':'\u01E7',
                 r'\v{K}':'\u01E8', r'{\v K}':'\u01E8', r'\v{k}':'\u01E9', r'{\v k}':'\u01E9'}
        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    if (r'\H' in s):
        trans = {r'\H{O}':u'Ő',  r'\H{o}':u'ő',  r'\H{U}':u'Ű',  r'\H{u}':u'ű',
                 r'{\H O}':u'Ő', r'{\H o}':u'ő', r'{\H U}':u'Ű', r'{\H u}':u'ű'}
        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Characters with a ring above.
    if (r'\r' in s):
        trans = {r'\r{U}':u'Ů', r'{\r U}':u'Ů', r'\r{u}':u'ů', r'{\r u}':u'ů'}
        for c in trans:
            if c in s: s = s.replace(c, trans[c])

    ## Now let's do the straightforward accent characters.
    trans = {r'\`A':u'\u00C1',  r'\`a':u'\u00E0',  r"\'A":u'\u00C1', r"\'a":u'\u00E1',
             r'\~A':u'\u00C3',  r'\^a':u'\u00E2',  r'\"A':u'\u00C4', r'\~a':u'\u00E3',
             r'\"a':u'\u00E4',  r'\`E':u'\u00C8',  r"\'E":u'\u00C9', r'\`e':u'\u00E8',
             r'\^E':u'\u00CA',  r"\'e":u'\u00E9',  r'\"E':u'\u00CB', r'\^e':u'\u00EA',
             r'\`I':u'\u00CC',  r'\"e':u'\u00EB',  r"\'I":u'\u00CD', r'\`\i':u'\u00EC',
             r'\^I':u'\u00CE',  r"\'\i":u'\u00ED', r'\"I':u'\u00CF', r'\^\i':u'\u00EE',
             r'\~N':u'\u00D1',  r'\"\i':u'\u00EF', r'\`O':u'\u00D2', r'\~n':u'\u00F1',
             r"\'O":u'\u00D3',  r'\`o':u'\u00F2',  r'\^O':u'\u00D4', r"\'o":u'\u00F3',
             r'\~O':u'\u00D5',  r'\^o':u'\u00F4',  r'\"O':u'\u00D6', r'\~o':u'\u00F5',
             r'\"o':u'\u00F6',  r'\`U':u'\u00D9',  r"\'U":u'\u00DA', r'\`u':u'\u00F9',
             r'\^U':u'\u00DB',  r"\'u":u'\u00FA',  r'\"U':u'\u00DC', r'\^u':u'\u00FB',
             r"\'Y":u'\u00DD',  r'\"u':u'\u00FC',  r"\'y":u'\u00FD', r'\"y':u'\u00FF',
             r'\=A':u'\u0100',  r'\=a':u'\u0101',  r"\'C":u'\u0106', r"\'c":u'\u0107',
             r'\^C':u'\u0108',  r'\^c':u'\u0109',  r'\.C':u'\u010A', r'\.c':u'\u010B',
             r'\=E':u'\u0112',  r'\=e':u'\u0113',  r'\.E':u'\u0116', r'\.e':u'\u0117',
             r'\^G':u'\u011C',  r'\^g':u'\u011D',  r'\.G':u'\u0120', r'\.g':u'\u0121',
             r'\^H':u'\u0124',  r'\^h':u'\u0125',  r'\~I':u'\u0128', r'\~\i':u'\u0129',
             r'\=I':u'\u012A',  r'\=\i':u'\u012B', r'\.I':u'\u0130', r'\^J':u'\u0134',
             r'\^\j':u'\u0135', r"\'L":u'\u0139',  r"\'N":u'\u0143', r"\'n":u'\u0144',
             r'\=O':u'\u014C',  r'\=o':u'\u014D',  r"\'R":u'\u0154', r"\'r":u'\u0155',
             r"\'S":u'\u015A',  r"\'s":u'\u015B',  r'\~U':u'\u0168', r'\~u':u'\u0169',
             r'\=U':u'\u016A',  r'\=u':u'\u016B',  r'\^W':u'\u0174', r'\^w':u'\u0175',
             r'\^Y':u'\u0176',  r'\^y':u'\u0177',  r"\'Z":u'\u0179', r"\'z":u'\u017A',
             r'\.Z':u'\u017B',  r'\.z':u'\u017C',
             r'\`Y':u'Ỳ',       r'\`y':u'ỳ',       r"\'K":u'Ḱ',      r"\'k":u'ḱ',
             r"\'l":u'ĺ',       r'\^A':u'Â',       r'\^S':u'Ŝ',      r'\^s':u'ŝ',
             r'\"Y':u'Ÿ',       r'\~E':u'Ẽ',       r'\~e':u'ẽ',      r'\~Y':u'Ỹ',
             r'\~y':u'ỹ'}

    for c in trans:
        if c in s: s = s.replace(c, trans[c])

    ## Do again for anyone using extra braces.
    trans = {r'\`{A}':u'\u00C1',  r'\`{a}':u'\u00E0',  r"\'{A}":u'\u00C1', r"\'{a}":u'\u00E1',
             r'\~{A}':u'\u00C3',  r'\^{a}':u'\u00E2',  r'\"{A}':u'\u00C4', r'\~{a}':u'\u00E3',
             r'\"{a}':u'\u00E4',  r'\`{E}':u'\u00C8',  r"\'{E}":u'\u00C9', r'\`{e}':u'\u00E8',
             r'\^{E}':u'\u00CA',  r"\'{e}":u'\u00E9',  r'\"{E}':u'\u00CB', r'\^{e}':u'\u00EA',
             r'\`{I}':u'\u00CC',  r'\"{e}':u'\u00EB',  r"\'{I}":u'\u00CD', r'\`{\i}':u'\u00EC',
             r'\^{I}':u'\u00CE',  r"\'{\i}":u'\u00ED', r'\"{I}':u'\u00CF', r'\^{\i}':u'\u00EE',
             r'\~{N}':u'\u00D1',  r'\"{\i}':u'\u00EF', r'\`{O}':u'\u00D2', r'\~{n}':u'\u00F1',
             r"\'{O}":u'\u00D3',  r'\`{o}':u'\u00F2',  r'\^{O}':u'\u00D4', r"\'{o}":u'\u00F3',
             r'\~{O}':u'\u00D5',  r'\^{o}':u'\u00F4',  r'\"{O}':u'\u00D6', r'\~{o}':u'\u00F5',
             r'\"{o}':u'\u00F6',  r'\`{U}':u'\u00D9',  r"\'{U}":u'\u00DA', r'\`{u}':u'\u00F9',
             r'\^{U}':u'\u00DB',  r"\'{u}":u'\u00FA',  r'\"{U}':u'\u00DC', r'\^{u}':u'\u00FB',
             r"\'{Y}":u'\u00DD',  r'\"{u}':u'\u00FC',  r"\'{y}":u'\u00FD', r'\"{y}':u'\u00FF',
             r'\={A}':u'\u0100',  r'\={a}':u'\u0101',  r"\'{C}":u'\u0106', r"\'{c}":u'\u0107',
             r'\^{C}':u'\u0108',  r'\^{c}':u'\u0109',  r'\.{C}':u'\u010A', r'\.{c}':u'\u010B',
             r'\={E}':u'\u0112',  r'\={e}':u'\u0113',  r'\.{E}':u'\u0116', r'\.{e}':u'\u0117',
             r'\^{G}':u'\u011C',  r'\^{g}':u'\u011D',  r'\.{G}':u'\u0120', r'\.{g}':u'\u0121',
             r'\^{H}':u'\u0124',  r'\^{h}':u'\u0125',  r'\~{I}':u'\u0128', r'\~{\i}':u'\u0129',
             r'\={I}':u'\u012A',  r'\={\i}':u'\u012B', r'\.{I}':u'\u0130', r'\^{J}':u'\u0134',
             r'\^{\j}':u'\u0135', r"\'{L}":u'\u0139',  r"\'{N}":u'\u0143', r"\'{n}":u'\u0144',
             r'\={O}':u'\u014C',  r'\={o}':u'\u014D',  r"\'{R}":u'\u0154', r"\'{r}":u'\u0155',
             r"\'{S}":u'\u015A',  r"\'{s}":u'\u015B',  r'\~{U}':u'\u0168', r'\~{u}':u'\u0169',
             r'\={U}':u'\u016A',  r'\={u}':u'\u016B',  r'\^{W}':u'\u0174', r'\^{w}':u'\u0175',
             r'\^{Y}':u'\u0176',  r'\^{y}':u'\u0177',  r"\'{Z}":u'\u0179', r"\'{z}":u'\u017A',
             r'\.{Z}':u'\u017B',  r'\.{z}':u'\u017C',
             r'\`{Y}':u'Ỳ',       r'\`{y}':u'ỳ',       r"\'{K}":u'Ḱ',      r"\'{k}":u'ḱ',
             r"\'{l}":u'ĺ',       r'\^{A}':u'Â',       r'\^{S}':u'Ŝ',      r'\^{s}':u'ŝ',
             r'\"{Y}':u'Ÿ',       r'\~{E}':u'Ẽ',       r'\~{e}':u'ẽ',      r'\~{Y}':u'Ỹ',
             r'\~{y}':u'ỹ'}

    for c in trans:
        if c in s: s = s.replace(c, trans[c])

    ## Those were easy. Next we look for single-char codes that must be followed by a non-alpha
    ## element, so that for example \orange will produce the "\orange" LaTeX command while
    ## "{\o}range" or "\o range" will produce "ørange". Since we're using regex and not Python's
    ## string objects, we need to replace all backslashes with double-backslashes. Thankfully,
    ## no other regex escape characters occur in this list of LaTeX markup for foreign letters.
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
def parse_bst_template_str(bst_template_str, bibentry, variables, undefstr='???'):
    '''
    From an "options train" `[...|...|...]`, find the first fully defined block in the
    train.

    A Bibulous type of bibliography style template string contains grammatical featues
    called options trains, of the form `[...|...|...]`. Each "block" in the train (divided
    from the others by a `|` symbol), contains fields which, if defined, replace the
    entire options train in the returned string.

    Parameters
    ----------
    bst_template_str : str
        The string containing a complete entrytype bibliography style template.
    variables : list of str
        The list of variables defined within the template string.
    bibentry : dict
        An entry from the bibliography database.
    undefstr : str
        The string to replace undefined required fields with.

    Returns
    -------
    arg : str
          The string giving the entrytype block to replace an options train.

    Example
    -------
    parse_bst_template_str() is given an options train "[<title>|<booktitle>]" and begins to
    look into the bibliography entry. It does not find a "title" entry but does find a "booktitle"
    entry. So, the function returns "<booktitle>", thereby replacing the train with the proper
    defined variable.
    '''

    ## Divide up the format string into
    block_train = bst_template_str.split('|')
    nblocks = len(block_train)

    ## Go through the if/elseif/else train of blocks within the string one by one. In each block,
    ## see if there are any variables defined. If no variables are present, then the
    ## block is "defined" and we return that block (i.e. replacing the train with that block). If
    ## an argument is defined, strip its surrounding '<' and '>' and look to see if the variable is
    ## defined in the bibdata entry. If so, the variable is defined and we return the '<var>'
    ## version of the variable (later code will do the variable replacement). If the variable is
    ## undefined (not present in the bibdata entry) then skip to the next block. If there is no
    ## next block, or if the block is empty (which means undefined by definition) then set the
    ## result to be the "undefined string".
    for i in range(nblocks):
        block = block_train[i]
        if (block == ''):
            #print('Required block "' + block + '" in "[' + bst_template_str + ']" is undefined.')
            arg = undefstr
            break

        ## If no variable exists inside the options-block, then just copy the text inside the
        ## block.
        if ('<' not in block):
            arg = block
            break

        ## Count how many variables there are in the block.
        block_variables = [v for v in variables if v in block]
        block_is_fully_defined = True

        ## Loop through the list of variables and find which ones are defined within the
        ## bibliography entry.
        for var in block_variables:
            varname = var[1:-1]             ## remove the angle brackets
            if (varname in bibentry):
                block_is_fully_defined = (bibentry[varname] != None)
            else:
                block_is_fully_defined = False

            if not block_is_fully_defined: break

        ## If after going through all of the variables in a block, we have located definitions for
        ## all of them, then the entire block is defined, and we can return it without evaluating
        ## the next block.
        if block_is_fully_defined:
            arg = block
            break
        else:
            arg = ''

    return(arg)

## =============================
def namestr_to_namedict(namestr, disable=None):
    '''
    Take a BibTeX string representing a single person's name and parse it into its first, middle, \
    last, etc pieces.

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

    ## First, if there is a comma within the string, then build the delimiter level list so you
    ## can check whether the comma is at delimiter level 0 (and therefore a valid comma for
    ## determining name structure). Using this, determine the locations of "valid" commas.
    if (',' in namestr):
        z = get_delim_levels(namestr, ('{','}'))
        commapos = []
        for match in re.finditer(',', namestr):
            i = match.start()
            if (z[i] == 0): commapos.append(i)
    else:
        commapos = []

    ## Note: switch on "len(commapos)" here rather than on "(',' not in namestr)" because the
    ## latter will produce an error when the comma occurs at brace levels other than zero.
    if (len(commapos) == 0):
        ## Allow nametokens to be split by spaces *or* word ties ('~' == unbreakable spaces),
        ## except when the '~' is preceded by a backslash, in which case we have the LaTeX markup
        ## for the tilde accent. We use "stringsplit()" rather than the standard
        ## string object's "split()" function because we don't want the split to be applied when
        ## the separator is not at brace level zero.
        nametokens = stringsplit(namestr, r' |(?<!\\)~')

        for n in nametokens:
            n_temp = n.strip('{').strip('}')[:-1]
            ## If we find a dot which is not preceded by a backslash and not succeeded by a dash.
            ## Also, we shouldn't care about dots appearing within curle braces, so we have to
            ## check for that as well.
            z = get_delim_levels(namestr, ('{','}'))
            for match in re.finditer(r'(?<!\\)\.(?!-)', n_temp):
                i = match.start()
                if (z[i] == 0):
                    warn('Warning 021: The name token "' + n + '" in namestring "' + namestr + \
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
        first_nametokens = firstpart.strip().split(' ')
        second_nametokens = secondpart.strip().split(' ')

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
            warn('Warning 022: the BibTeX format for namestr="' + namestr + '" is malformed.' + \
                 '\nThere should be only one name in the second part of the three comma-' \
                 'separated name elements.', disable)
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
        warn('Warning 023: the BibTeX format for namestr="' + namestr + '" is malformed.' + \
             '\nThere should never be more than four commas in a given name.', disable)
        return({'last':'???'})

    ## If any tokens in the middle name start with lower case, then move them, and any tokens after
    ## them, to the prefix. An important difference is that prefixes typically don't get converted
    ## to initials when generating the formatted bibliography string.
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

    return(namedict)

## ===================================
def search_middlename_for_prefixes(namedict):
    '''
    From the middle name of a single person, check if any of the names should be placed into the
    "prefix" and move them there.

    Parameters
    ----------
    namedict : dict
        The dictionary containing the key "middle", containing the string with the person's \
        middle names/initials.

    Returns
    -------
    namedict : dict
        The dictionary augmented with the key "prefix" if a prefix is indeed found.
    '''

    if ('middle' not in namedict):
        return(namedict)

    ## Search the list of middle names from the back to the front. If the name encountered starts
    ## with lower case, then it is moved to namedict['prefix']. If not, then stop the search and
    ## break out of the loop.
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
def create_edition_ordinal(bibentry, disable=None):
    '''
    Given a bibliography entry's edition *number*, format it as an ordinal (i.e. "1st", "2nd" \
    instead of "1", "2") in the way that it will appear on the formatted page.

    Parameters
    ----------
    bibentry : dict
        The bibliography database entry.
    disable : list of int, optional
        The list of warning message numbers to ignore.

    Returns
    -------
    editionstr : str
        The formatted form of the edition, with ordinal attached.
    '''

    ## First check that the key exists.
    if ('edition' not in bibentry):
        return(None)

    if not bibentry['edition'].isdigit():
        return(bibentry['edition'])

    edition_number = bibentry['edition']
    trans = {'first':'1', 'second':'2', 'third':'3', 'fourth':'4', 'fifth':'5', 'sixth':'6',
             'seventh':'7', 'eighth':'8', 'ninth':'10', 'tenth':'10', 'eleventh':'11',
             'twelfth':'12', 'thirteenth':'13', 'fourteenth':'14', 'fifteenth':'15',
             'sixteenth':'16', 'seventeenth':'17', 'eighteenth':'18', 'nineteenth':'19',
             'twentieth':'20'}

    if edition_number.lower() in trans:
        edition_number = trans[edition_number.lower()]

    ## Add the ordinal string to the number.
    if (edition_number == '1'):
        editionstr = '1st'
    elif (edition_number == '2'):
        editionstr = '2nd'
    elif (edition_number == '3'):
        editionstr = '3rd'
    elif (int(edition_number) > 3):
        editionstr = edition_number + 'th'
    else:
        if ('edition' in bibentry):
            warn('Warning 024: the edition number "' + unicode(edition_number) + '" given for ' + \
                 'entry ' + key + ' is invalid. Ignoring', disable)
            editionstr = options['undefstr']

    return(editionstr)

## =============================
def export_bibfile(bibdata, filename):
    '''
    Write a bibliography database dictionary into a .bib file.

    Parameters
    ----------
    filename : str
        The filename of the file to write.
    bibdata : dict
        The bibliography dictionary to write out.
    '''

    assert isinstance(filename, basestring), 'Input "filename" must be a string.'
    f = open(filename, 'w')

    for key in bibdata:
        entry = bibdata[key]
        f.write('@' + entry['entrytype'].upper() + '{' + key + ',\n')
        del bibdata[key]['entrytype']
        nkeys = len(entry.keys())

        ## Write out the entries.
        for i,k in enumerate(entry):
            f.write('  ' + k + ' = {' + unicode(entry[k]) + '}')

            ## If this is the last field in the dictionary, then do not end the line with a
            ## trailing comma.
            if (i == (nkeys-1)):
                f.write('\n')
            else:
                f.write(',\n')

        f.write('}\n\n')

    f.close()
    return

## =============================
def parse_pagerange(pages_str, citekey=None, disable=None):
    '''
    Given a string containing the "pages" field of a bibliographic entry, figure out the start and
    end pages.

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

    ## Note that we work with strings instead of integers, because the use of letters in article
    ## pages is common (e.g. page "D5").
    if ('-' in pages_str) or (',' in pages_str):
        pagesplit = multisplit(pages_str, ('-',','))
        startpage = pagesplit[0].strip()
        endpage = pagesplit[-1].strip()
        if (endpage == startpage): endpage = None
    else:
        startpage = pages_str
        endpage = None

    ## For user convenience, add a check here that if endpage and startpages are both numbers and
    ## endpage <= startpage, then there is a typo.
    if startpage.isdigit() and endpage and endpage.isdigit():
        if int(endpage) < int(startpage):
            if (citekey != None):
                warn('Warning 025a: the "pages" field in entry "' + citekey + '" has a malformed '
                     'page range (endpage < startpage). Ignoring ...', disable)
            else:
                warn('Warning 025b: the "pages" field "' + pages_str + '" is malformed, since '
                     'endpage < startpage. Ignoring ...', disable)

    return(startpage, endpage)

## =============================
def parse_nameabbrev(abbrevstr):
    '''
    Given a string containing either a single "name" > "abbreviation" pair or a list of such pairs,
    parse the string into a dictionary of names and abbreviations.

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
def make_sortkey_unique(sortkey, sortdict):
    '''
    Given a key that matches an already-present key in the input dictionary, generate a new key by
    appending zeros to the key string.

    Parameters
    ----------
    sortkey : str
        The key to be modified.
    sortdict : dict
        The dictionary whose keys we can query to check for uniqueness.

    Returns
    -------
    newkey : str
        The new (and unique) key.
    '''

    if (sortkey not in sortdict):
        return(sortkey)

    newkey = sortkey
    while True:
        newkey += '0'
        if (newkey not in sortdict):
            break

    return(newkey)

## =============================
def filter_script(line):
    '''
    Remove elements from a Python script which are provide the most egregious security flaws; also
    replace some identifiers with their correct namespace representation.

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
    #identifier_pattern = re.compile(r'[A-Za-z_]\w+', re.UNICODE)
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
    Check is an input string represents an integer value. Although a trivial function, it will be
    useful for user scripts.

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
        value = int(s)
        return(True)
    except ValueError:
        return(False)

## =============================
def warn(msg, disable=None):
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

    ## For each number in the "ignore" list, find out if the warning message is one of the ones to
    ## ignore. If so, then do nothing.
    show_warning = True
    for i in disable:
        s = ('Warning %03i' % i)
        if msg.startswith(s):
            show_warning = False
            break

    if show_warning:
        print(msg)

    return


## ==================================================================================================

if (__name__ == '__main__'):
    print('sys.argv=', sys.argv)
    if (len(sys.argv) > 1):
        try:
            (opts, args) = getopt.getopt(sys.argv[1:], '', ['locale='])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err) # will print something like "option -a not recognized"
            ## Add some print statements here telling the user the basic interface to the function.
            sys.exit(2)

        for o,a in opts:
            if (o == '--locale'):
                locale = a
            else:
                assert False, "unhandled option"

        ## Use this command on the command line:
        #/home/nh/Lab\ Notes/Bibulous/biblatex.py /home/nh/Publications/2013\ OE\ -\ Review\ of\ Snapshot/snapshot_review.tex /home/nh/Lab\ Notes/Bibulous/osa.bst
        #arg_texfile = sys.argv[0]
        arg_auxfile = args[0]
        #if (arg_texfile[0] != '/'):
        #    arg_texfile = os.getcwd() + '/' + arg_texfile
        #files = [arg_texfile, arg_auxfile]
        files = arg_auxfile
    else:
        ## Use the test example input.
        arg_bibfile = './test/test1.bib'
        arg_auxfile = './test/test1.aux'
        arg_bstfile = './test/test1.bst'
        files = [arg_bibfile, arg_auxfile, arg_bstfile]

    bibdata = Bibdata(files, debug=False)
    bibdata.write_bblfile()
    print('Writing to BBL file = ' + bibdata.filedict['bbl'])
    #os.system('kwrite ' + bibdata.filedict['bbl'])


    print('DONE')

