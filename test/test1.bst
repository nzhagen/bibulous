TEMPLATES:
initialize1 = <authorliststr>, \enquote{<title>} (<year>).
initialize2 = <authorliststr>, \enquote{<title>} (<year>).
title_punctuation = <authorliststr>, \enquote{<title>,} (<year>).
quote_delimits = <authorliststr>, \enquote{<title>} (<year>).
page_range = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
nested_italics1 = <authorliststr>, \textit{<title>} (<year>).
nested_italics2 = \enquote{<title1>}, \enquote{<title2>}.
nested_bold = \enquote{<title1>}, \enquote{<title2>}.
nested_quotes = \enquote{<title1>}, \enquote{<title2>}, \enquote{<title3>}, \enquote{<title4>}, \enquote{<title5>}.
name_parsing1 = <authorliststr>, \enquote{<title>} (<year>).
name_parsing2 = <authorliststr>, \enquote{<title>} (<year>).
name_parsing3 = <authorliststr>, \enquote{<title>} (<year>).
many_authors = <authorliststr>, \enquote{<title>} (<year>).
many_editors = <editorliststr>, \enquote{<title>} (<year>).
name_abbrev1 = <authorliststr>, \enquote{<title>} (<year>).
name_abbrev2 = <authorliststr>, \enquote{<title>} (<year>).
brace_delimited_quotes = <authorliststr>, \enquote{<title>} (<year>).
inproceedings = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <eid> (<year>).
article = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <eid> (<year>).
crossref = <authorliststr>, \enquote{<title>,} in \textit{<booktitle>}, <editorliststr>, Proc. SPIE \textbf{<volume>}: <eid> (<year>).
japanese = <authorliststr>, \enquote{<title>,} <publisher> (<year>). {\makeopenbracket}In <language>.{\makeclosebracket}
trailing_comma = <authorliststr>, \enquote{<title>} (<year>).
monthformat1 = <authorliststr>, \enquote{<title>} (<monthname>, <year>).
monthformat2 = <authorliststr>, \enquote{<title>} (<monthname>, <year>).
monthformat3 = <authorliststr>, \enquote{<title>} (<month>, <year>).
replace_newlines = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
quote_and_accent_detection = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
hyperlinked_title = <authorliststr>, \enquote{[\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|],} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).

OPTIONS:
citation_order = citenum                  ## order the bibliography by "citekey" or "citenum" (or "nyt" etc.)
maxauthors = 9                            ## if more than 10 authors, then use "et al." format
minauthors = 7                            ## if "maxauthors" exceeded, then display only the first "minauthors" and et al.
maxeditors = 3                            ## if more than 5 editors, then use "et al." format
mineditors = 3                            ## if "maxeditors" exceeded, then display only the first "mineditors" and et al.
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
french_initials = False                   ## whether to use French initials (i.e. Jean-Paul -> J.-P. and not J., also Philippe -> Ph. not P.)
sort_with_prefix = False                  ## whether or not to use a person's prefix in front of the last name for sorting order. Should probably be used with option "sort_case=True".
period_after_initial = True               ## whether to add a '.' after a person's initials.
terse_inits = False                       ## whether to format initials as, for example, "DE" rather than "D. E."
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
month_abbrev = True                       ## whether to use abbreviated month names (i.e. "Jan" instead of "January").
use_name_ties = False                     ## whether to use ties ('~') instead of spaces to glue together initials.
replace_newlines = True                   ## whether to remove newlines from the database entry fields
missing_data_exceptions = False           ## whether to raise an exception when Bibulous finds a missing but required field.
undefstr = ???                            ## what string to replace undefined required fields with
force_sentence_case = False               ## Whether to reduce all but the first letter (and brace-protected letters) to lower case
authorlist_format = first_name_first      ## use authorlist "Bugs Bunny, Daffy Duck, and Porky Pig" format
use_firstname_initials = True             ## initialize all but the authors' last names
editorlist_format = first_name_first      ## use editorlist "Bugs Bunny, Daffy Duck, and Porky Pig" format
namelist_format = first_name_first        ## defines values for both "authorlist_format" and "editorlist_format" at once
use_name_ties = False                     ## whether or not to tie together initials with unbreaskable spaces ('~')

VARIABLES:

DEFINITIONS:
