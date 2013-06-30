TEMPLATES:
article = <authorliststr>, ``[\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|],'' \textit{<journal>} \textbf{<volume>}: [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).[ <note>]
book = [<authorliststr>|<editorliststr>|<organization>|<institution>|], \textit{<title>}[, <edition_ordinal>~ed.][, vol.~<volume>] (<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
endnote = <note>
inbook = incollection
incollection = <authorliststr>, ``<title>,'' in \textit{<booktitle>}, [vol.~<volume>, ][<edition_ordinal>~ed., ][<editorliststr>, ][<series>, ][Chap.~<chapter>, ][pp.~<startpage>--<endpage>|<eid>|] (<publisher>, <year>).[ <note>]
inproceedings = <authorliststr>, ``<title>,'' in \textit{<booktitle>}[, <editorliststr>][, in <series>][ \textbf{<volume>}][, pp.~<startpage>--<endpage>|, <eid>] (<year>). [<note>]
manual = [<authorliststr>|<editorliststr>|<organization>|<institution>|], \textit{<title>}, [vol.~<volume>, ][<edition_ordinal>~ed., |ver.~<version>, ][<editorliststr>, ] (<organization>, <year>)[, Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
mastersthesis = <authorliststr>, ``<title>,'' M.S. dissertation (<school>, <year>).[ <note>]
misc = [<authorliststr>, ][``<title>''][ (<organization>, <year>)| (<year>)].[ <note>]
patent = <authorliststr>, ``<title>,'' <nationality> patent <number> (<year>).[ <note>]
phdthesis = <authorliststr>, ``<title>,'' Ph.D. dissertation (<school>, <year>).[ <note>]
proceedings = <editorliststr>, \textit{<title>}, [vol.~<volume>][, <edition_ordinal>~ed.] (<year>).[ <note>]
techreport = [<authorliststr>, |<editorliststr>, ]``<title>,'' <institution>, Tech.\ Report <number> (<year>).[ <note>]
unpublished = misc

OPTIONS:
citation_sort = citekey                   ## order the reference list by "citekey" or "citenum" (or "nyt" etc.)
citation_label = citekey                  ## label the reference items by their numerical order of appearance
maxauthors = 9                            ## if more than 10 authors, then use "et al." format
minauthors = 9                            ## if "maxauthors" is exceeded, then display only the first "minauthors" and et al.
maxeditors = 5                            ## if more than 5 editors, then use "et al." format
mineditors = 5                            ## if "maxeditors" is exceeded, then display only the first "mineditors" and et al.
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
use_abbrevs = True                        ## whether to use the abbreviation strings (mainly useful for debugging)
french_initials = False                   ## whether to use French initials (i.e. Jean-Paul -> J.-P. and not J., also Philippe -> Ph. not P.)
sort_with_prefix = False                  ## whether or not to use a person's prefix in front of the last name for sorting order. Should probably be used with option "sort_case=True".
period_after_initial = True               ## whether to add a '.' after a person's initials.
terse_inits = False                       ## whether to format initials as, for example, "DE" rather than "D. E."
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
missing_data_exceptions = False           ## whether to raise an exception when Bibulous finds a missing but required field.
undefstr = ???                            ## what string to replace undefined required fields with
force_sentence_case = False               ## Whether to reduce all but the first letter (and brace-protected letters) to lower case
namelist_format = first_name_first        ## use authorlist (or editorlist) "Bugs Bunny, Daffy Duck, and Porky Pig" format
use_firstname_initials = True             ## initialize all but the authors' last names
namelist_format = first_name_first        ## defines values for both "authorlist_format" and "editorlist_format" at once
use_name_ties = False                     ## whether or not to tie together initials with unbreakable spaces ('~')
replace_newlines = True                   ## whether to replace newline characters inside fields with spaces
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")

VARIABLES:

DEFINITIONS:
