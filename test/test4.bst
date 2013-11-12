TEMPLATES:
article = <au>, \enquote{<title>} (<year>).
incollection = <au>, \enquote{<title>,} [in <booktitle>, ]<publisher> (<year>).[ {\makeopenbracket}In <language>.{\makeclosebracket}]


SPECIAL-TEMPLATES:
author = <author-en>
authorlist = <author.to_namelist()>
title = [<title-ja>|<title-en>|]
publisher = [<publisher-ja>|<publisher-en>|]
authorname.n = [<authorlist.n.first.initial()>. ][<authorlist.n.middle.initial()>. ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
au = <authorname.0>, ...,{ and }<authorname.6>
citelabel = None
sortkey = <citenum>


OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
replace_newlines = True                   ## whether to remove newlines from the database entry fields
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs
etal_message = , \textit{et al.}          ## what text to place at the end of a namelist when there are too many names
eds_message = {, ed.}{, eds}              ## the label to use after the editor namelist


VARIABLES:

DEFINITIONS:
