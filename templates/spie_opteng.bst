TEMPLATES:
article = <authorliststr>, \enquote{<title>,} [\href{<url>}{\textit{<journal>}}|\href{<doi>}{\textit{<journal>}}|\textit{<journal>}] \textbf{<volume>}(<number>), [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).[ <note>]
book = [<authorliststr>|<editorliststr>|<organization>|<institution>|], \textit{<title>}[, <edition_ordinal>~ed.][, vol.~<volume>] <publisher>, <address> (<year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>|, p.~<startpage>].[ <note>]
endnote = Warning (entry <citekey>): Opt.\ Eng.\ does not allow endnotes.
inbook = incollection
incollection = <authorliststr>, \enquote{<title>,} in \textit{<booktitle>}, [vol.~<volume>, ][<edition_ordinal>~ed., ][<editorliststr>, ][<series>, ][Chap.~<chapter>, ][pp.~<startpage>--<endpage>|p.~<startpage>|<eid>|] (<publisher>, <year>).[ <note>]
inproceedings = <authorliststr>, \enquote{<title>,} in \textit{<booktitle>}[, <editorliststr>][, in <series>][ \textbf{<volume>}][, pp.~<startpage>--<endpage>|, p.~<startpage>|, <eid>] (<year>).[ <note>]
manual = [<authorliststr>|<editorliststr>|<organization>|<institution>|], \textit{<title>}, [vol.~<volume>, ][<edition_ordinal>~ed., |ver.~\version, ][<editorliststr>, ] (<organization>, <year>)[, Chap.~<chapter>][, pp.~<startpage>--<endpage>|, p.~<startpage>].[ <note>]
mastersthesis = <authorliststr>, \enquote{<title>,} M.S. dissertation (<school>, <year>).[ <note>]
misc = [<authorliststr>, ][\enquote{<title>}][ (<organization>, <year>)| (<year>)].[ <note>]
patent = <authorliststr>, \enquote{<title>,} <nationality> patent <number> (<year>).[ <note>]
phdthesis = <authorliststr>, \enquote{<title>,} Ph.D. dissertation (<school>, <year>).[ <note>]
proceedings = <editorliststr>, \textit{<title>}, [vol.~<volume>][, <edition_ordinal>~ed.] (<year>).[ <note>]
techreport = [<authorliststr>|<editorliststr>|<organization>|<institution>|], \enquote{<title>,} <institution>, <number> (<year>).[ <note>]
website = \href{[<url>|<doi>]}{[<url>|<doi>]}

SPECIAL-TEMPLATES:
sortkey = <citenum>                       ## order the reference list in the same order as the citations were given in
citelabel = <citenum>                     ## use numeric reference labels

OPTIONS:
maxauthors = 3                            ## if more than 3 authors, then use "et al." format
minauthors = 1                            ## if "maxauthors" is exceeded, then display only the first "minauthors" and et al.
maxeditors = 3                            ## if more than 3 editors, then use "et al." format
mineditors = 1                            ## if "maxeditors" is exceeded, then display only the first "mineditors" and et al.
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
use_abbrevs = True                        ## whether to use the abbreviation strings (mainly useful for debugging)
french_initials = False                   ## whether to use French initials (i.e. Jean-Paul -> J.-P. and not J., also Philippe -> Ph. not P.)
period_after_initial = True               ## whether to add a '.' after a person's initials.
terse_inits = False                       ## whether to format initials as, for example, "DE" rather than "D. E.". This setting overrides the "period_after_initial" option.
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
month_abbrev = True                       ## whether to use abbreviated month names (i.e. "Jan" instead of "January").

## The remaining exceptions below are really for users rather than for the journal. Maybe put these someplace else?
undefstr = ???                            ## what string to replace undefined required fields with
force_sentence_case = False               ## whether to reduce all but the first letter (and brace-protected letters) to lower case
namelist_format = first_name_first        ## use authorlist (or editorlist) "Bugs Bunny, Daffy Duck, and Porky Pig" format
use_firstname_initials = True             ## initialize all but the authors' last names
namelist_format = first_name_first        ## defines values for both "authorlist_format" and "editorlist_format" at once
use_name_ties = False                     ## whether or not to tie together initials with unbreakable spaces ('~')
replace_newlines = True                   ## whether to replace newline characters inside fields with spaces
allow_scrips = False                      ## whether to allow user scripts in BST files
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")

VARIABLES:

DEFINITIONS:
