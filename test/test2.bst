#! /usr/bin/env bibulous

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

options.citation_order = citekey                                ## order the bibliography by "citekey" or "citenum" (or "nyt" etc.)
options.maxauthors = 9                                          ## if more than 10 authors, then use "et al." format
options.minauthors = 9                                          ## if "maxauthors" exceeded, then display only the first "minauthors" and et al.
options.maxeditors = 5                                          ## if more than 5 editors, then use "et al." format
options.mineditors = 5                                          ## if "maxeditors" exceeded, then display only the first "mineditors" and et al.
options.procspie_as_journal = True                              ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
options.sort_case = False                                       ## whether to use case-sensitive citation sorting (default is False)
options.warnings = True                                         ## whether to print warning strings
options.backrefs = False                                        ## whether to implement backreferences in the bibliography -- maybe put in template strings?
options.backrefstyle = none                                     ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
options.hyperref = False                                        ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
options.use_abbrevs = True                                      ## whether to use the abbreviation strings (mainly useful for debugging)
options.french_initials = False                                 ## whether to use French initials (i.e. Jean-Paul -> J.-P. and not J., also Philippe -> Ph. not P.)
options.sort_with_prefix = False                                ## whether or not to use a person's prefix in front of the last name for sorting order. Should probably be used with options.sort_case=True.
options.period_after_initial = True                             ## whether to add a '.' after a person's initials.
options.terse_inits = False                                     ## whether to format initials as, for example, "DE" rather than "D. E."
options.bibitemsep = 0pt                                        ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.

## The remaining exceptions below are really for users rather than for the journal. Maybe put these someplace else?
options.missing_data_exceptions = False                         ## whether to raise an exception when Bibulous finds a missing but required field.
options.undefstr = ???                                          ## what string to replace undefined required fields with
options.force_sentence_case = False                             ## Whether to reduce all but the first letter (and brace-protected letters) to lower case

options.namelist_format = first_name_first                      ## use authorlist (or editorlist) "Bugs Bunny, Daffy Duck, and Porky Pig" format
options.use_firstname_initials = True                           ## initialize all but the authors' last names
options.namelist_format = first_name_first                      ## defines values for both "authorlist_format" and "editorlist_format" at once
options.use_name_ties = False                                   ## whether or not to tie together initials with unbreakable spaces ('~')
options.replace_newlines = True                                 ## whether to replace newline characters inside fields with spaces

