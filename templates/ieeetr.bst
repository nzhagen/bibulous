#! /usr/bin/env bibulous

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
techreport = <authorliststr>, \enquote{<title>,} Tech.\ Rep.\ <number>, [<institution>, |<organization, |]<publisher>, [<monthname> ]<year>.[ <note>]
unpublished = <authorliststr>, \enquote{<title>.}[ <note>,] [<monthname> ]<year>.

options.citation_order = citenum                                ## order the bibliography by "citekey" or "citenum" (or "nyt" etc.)
options.period_after_initial = True                             ## whether to add a '.' after a person's initials.
options.terse_inits = False                                     ## whether to format initials as, for example, "DE" rather than "D. E."
options.procspie_as_journal = False                             ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
options.sort_case = False                                       ## whether to use case-sensitive citation sorting (default is False)
options.backrefs = False                                        ## whether to implement backreferences in the bibliography -- maybe put in template strings?
options.backrefstyle = none                                     ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
options.hyperref = False                                        ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
options.use_abbrevs = True                                      ## whether to use the abbreviation strings (mainly useful for debugging)
options.warnings = True                                         ## whether to print warning strings
options.french_initials = False                                 ## whether to use French initials (i.e. Jean-Paul -> J.-P. and not J., also Philippe -> Ph. not P.)
options.sort_with_prefix = False                                ## whether or not to use a person's prefix in front of the last name for sorting order. Should probably be used with options.sort_case=True.
options.bibitemsep = 0pt                                        ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
options.namelist_format = first_name_first                      ## use authorlist (or editorlist) "Bugs Bunny, Daffy Duck, and Porky Pig" format
options.use_firstname_initials = True                           ## initialize all but the authors' last names
options.use_name_ties = False                                   ## whether or not to tie together initials with unbreakable spaces ('~')
options.replace_newlines = True                                 ## whether to replace newline characters inside fields with spaces
options.month_abbrev = True
options.maxauthors = 9                                          ## if more than 10 authors, then use "et al." format
options.minauthors = 9                                          ## if "maxauthors" exceeded, then display only the first "minauthors" and et al.
options.maxeditors = 5                                          ## if more than 5 editors, then use "et al." format
options.mineditors = 5                                          ## if "maxeditors" exceeded, then display only the first "mineditors" and et al.

## The remaining exceptions below are really for users rather than for the journal. Maybe put these someplace else?
options.missing_data_exceptions = False                         ## whether to raise an exception when Bibulous finds a missing but required field.
options.undefstr = ???                                          ## what string to replace undefined required fields with
options.use_csquotes = False                                    ## whether to use the \enquote{} command from LaTeX package "csquotes.sty" for formatting quotation marks.
options.force_sentence_case = False                             ## Whether to reduce all but the first letter (and brace-protected letters) to lower case


