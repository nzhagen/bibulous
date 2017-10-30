TEMPLATES:
article = [<au>|<ed>|], \enquote{<title>} (<year>).
incollection = [<au>|<ed.if_singular(editorlist, option.edmsg1, option.edmsg2)>|], \enquote{<title>,} [in <booktitle>, ]<publisher> (<year>).[ {\makeopenbracket}In <language>.{\makeclosebracket}]


SPECIAL-TEMPLATES:
author = <author-en>
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
title = [<title-ja>|<title-en>|]
publisher = [<publisher-ja>|<publisher-en>|]
authorname.n = [<authorlist.n.first.initial()>. ][<authorlist.n.middle.initial()>. ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
au = <authorname.0>, ...,{ and }<authorname.6>
editorname.n = [<editorlist.n.first.initial()>. ][<editorlist.n.middle.initial()>. ][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
ed = <editorname.0>, ...,{ and }<editorname.6>
citelabel = None
presortkey = [<sortname>|<authorlist.0.last>|<editorlist.0.last>|][<authorlist.0.first>|<editorlist.0.first>][<sortyear.zfill(4)>|<year.zfill(4)>][<sorttitle>|<title>]<citekey>
sortkey = <presortkey.purify().compress()>


OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = True
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
replace_newlines = True                   ## whether to remove newlines from the database entry fields
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs
etal_message = , \textit{et~al.}          ## what text to place at the end of a namelist when there are too many names
edmsg1 = , ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present
sort_order = Forward
wrap_nested_quotes = True                 ## whether to replace \enquote{} commands and adjust nested quotations


VARIABLES:

DEFINITIONS:
