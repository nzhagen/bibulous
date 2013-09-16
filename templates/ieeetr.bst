TEMPLATES:
article = <authorliststr>, \enquote{<title>,} \textit{<journal>} vol.~<volume>: [pp.~<startpage>--<endpage>|p.~<startpage>|<eid>|], [<monthname> ]<year>.[ <note>]
book = [<authorliststr>|<editorliststr>|<organization>|<institution>|], \textit{<title>}[, vol.~<volume>]. [<address>: ]<publisher>, [<edition_ordinal>~ed., ][<monthname> ]<year>.[ <note>]
booklet = <authorliststr>, \enquote{<title>.} [<howpublished>, ][<address>, ][<monthname> ]<year>.[ <note>]
conference = [<authorliststr>|<organization>|<institution>|], \enquote{<title>,} [in \textit{<booktitle>}][ (<editorliststr>, ed.), ][vol.~<volume>, ] (<address>)[, p.~<startpage>][, <organization>], <publisher>, [<monthname> ]<year>.[ <note>]
inbook = <authorliststr>, \textit{<title>}, [vol.~<volume>, ][ch.~<chapter>, ][pp.~<startpage>--<endpage>|<eid>|]. <address>: <publisher>, [<edition_ordinal>~ed., ][<monthname> ]<year>).[ <note>]
incollection = [<authorliststr>|<organization>|<institution>|], \enquote{<title>,} [in \textit{<booktitle>}][ (<editorliststr>, ed.), ][vol.~<volume>, ][ch.~<chapter>, ][pp.~<startpage>--<endpage>|<eid>|] <address>: <publisher>, [<edition_ordinal>~ed., ][<monthname> ]<year>.[ <note>]
manual = [<authorliststr>|<editorliststr>|], \textit{<title>}. [<organization>, ][<address>, ][<edition_ordinal>~ed., |ver.~<version>, ][<monthname> ]<year>).[ <note>]
mastersthesis = <authorliststr>, ``<title>,'' Master's thesis, <school>, <address>, [<monthname> ]<year>).[ <note>]
misc = <authorliststr>, \enquote{<title>.}[ <howpublished>, ]<monthname> ]<year>.[ <note>]
phdthesis = <authorliststr>, \textit{<title>}, Ph.D. thesis, <school>, <address>, [<monthrname> ]<year>.[ <note>]
proceedings = <editorliststr>, ed., \textit{<title>}, [vol.~<volume>, ][<organization>, ]<publisher> [<monthname> ]<year>.[ <note>]
techreport = <authorliststr>, \enquote{<title>,} Tech.\ Rep.\ <number>, [<institution>, |<organization>, |]<publisher>, [<monthname> ]<year>.[ <note>]
unpublished = <authorliststr>, \enquote{<title>.}[ <note>,] [<monthname> ]<year>.

SPECIAL-TEMPLATES:
sortkey = <citenum>                       ## order the reference list in the same order as the citations were given in
citelabel = <citenum>                     ## use numeric reference labels

OPTIONS:
maxauthors = 9                            ## if more than 10 authors, then use "et al." format
minauthors = 9                            ## if "maxauthors" exceeded, then display only the first "minauthors" and et al.
maxeditors = 5                            ## if more than 5 editors, then use "et al." format
mineditors = 5                            ## if "maxeditors" exceeded, then display only the first "mineditors" and et al.
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

