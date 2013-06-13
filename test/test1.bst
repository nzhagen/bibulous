#! /usr/bin/env bibulous

initialize1 = <authorliststr>, \enquote{<title>} (<year>).
initialize2 = <authorliststr>, \enquote{<title>} (<year>).
titlepunctuation1 = <authorliststr>, \enquote{<title>,} (<year>).
quotedelimits1 = <authorliststr>, \enquote{<title>} (<year>).
pagerange1 = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
nesteditalics1 = <authorliststr>, \textit{<title>} (<year>).
nestedbold1 = \enquote{<title1>}, \enquote{<title2>}.
nesteditalics2 = \enquote{<title1>}, \enquote{<title2>}.
nestedquotes1 = \enquote{<title1>}, \enquote{<title2>}, \enquote{<title3>}, \enquote{<title4>}, \enquote{<title5>}.
nameparsing1 = <authorliststr>, \enquote{<title>} (<year>).
nameparsing2 = <authorliststr>, \enquote{<title>} (<year>).
nameparsing3 = <authorliststr>, \enquote{<title>} (<year>).
manyauthors1 = <authorliststr>, \enquote{<title>} (<year>).
manyeditors1 = <editorliststr>, \enquote{<title>} (<year>).
nameabbrev1 = <authorliststr>, \enquote{<title>} (<year>).
nameabbrev2 = <authorliststr>, \enquote{<title>} (<year>).
bracedelimitedquotes1 = <authorliststr>, \enquote{<title>} (<year>).
inproceedings = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <eid> (<year>).
article = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <eid> (<year>).
crossref1 = <authorliststr>, \enquote{<title>,} in \textit{<booktitle>}, <editorliststr>, Proc. SPIE \textbf{<volume>}: <eid> (<year>).
japanese1 = <authorliststr>, \enquote{<title>,} <publisher> (<year>). {\makeopenbracket}In <language>.{\makeclosebracket}
trailingcomma1 = <authorliststr>, \enquote{<title>} (<year>).
monthformat1 = <authorliststr>, \enquote{<title>} (<monthname>, <year>).
monthformat2 = <authorliststr>, \enquote{<title>} (<monthname>, <year>).
monthformat3 = <authorliststr>, \enquote{<title>} (<month>, <year>).


options.citation_order = citenum                                ## order the bibliography by "citekey" or "citenum" (or "nyt" etc.)
options.maxauthors = 9                                          ## if more than 10 authors, then use "et al." format
options.minauthors = 7                                          ## if "maxauthors" exceeded, then display only the first "minauthors" and et al.
options.maxeditors = 3                                          ## if more than 5 editors, then use "et al." format
options.mineditors = 3                                          ## if "maxeditors" exceeded, then display only the first "mineditors" and et al.
options.procspie_as_journal = True                              ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
options.sort_case = False                                       ## whether to use case-sensitive citation sorting (default is False)
options.backrefs = False                                        ## whether to implement backreferences in the bibliography -- maybe put in template strings?
options.backrefstyle = none                                     ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
options.hyperref = False                                        ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
options.use_abbrevs = True                                      ## whether to use the abbreviation strings (mainly useful for debugging)
options.french_initials = False                                 ## whether to use French initials (i.e. Jean-Paul -> J.-P. and not J., also Philippe -> Ph. not P.)
options.sort_with_prefix = False                                ## whether or not to use a person's prefix in front of the last name for sorting order. Should probably be used with options.sort_case=True.
options.period_after_initial = True                             ## whether to add a '.' after a person's initials.
options.terseinits = False                                      ## whether to format initials as, for example, "DE" rather than "D. E."
options.bibitemsep = 0pt                                        ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
options.month_abbrev = True                                     ## whether to use abbreviated month names (i.e. "Jan" instead of "January").
options.use_name_ties = False                                   ## whether to use ties ('~') instead of spaces to glue together initials.

## The remaining exceptions below are really for users rather than for the journal. Maybe put these someplace else?
options.missing_data_exceptions = False                         ## whether to raise an exception when Bibulous finds a missing but required field.
options.undefstr = ???                                          ## what string to replace undefined required fields with
options.force_sentence_case = False                             ## Whether to reduce all but the first letter (and brace-protected letters) to lower case

options.authorlist_format = first_name_first                    ## use authorlist "Bugs Bunny, Daffy Duck, and Porky Pig" format
options.use_author_firstname_initials = True                    ## initialize all but the authors' last names
options.use_editor_firstname_initials = True                    ## initialize all but the editors' last names
options.editorlist_format = first_name_first                    ## use editorlist "Bugs Bunny, Daffy Duck, and Porky Pig" format
options.namelist_format = first_name_first                      ## defines values for both "authorlist_format" and "editorlist_format" at once
options.use_name_ties = False                                   ## whether or not to tie together initials with unbreaskable spaces ('~')

