TEMPLATES:
initialize1 = <au>, \enquote{<title>} (<year>).
initialize2 = <au>, \enquote{<title>} (<year>).
title_punctuation = <au>, \enquote{<title>,} (<year>).
quote_delimits = <au>, \enquote{<title>} (<year>).
page_range = <au>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
nested_italics1 = <au>, \textit{<title>} (<year>).
nested_italics2 = \enquote{<title1>}, \enquote{<title2>}.
nested_bold = \enquote{<title1>}, \enquote{<title2>}.
nested_quotes = \enquote{<title1>}, \enquote{<title2>}, \enquote{<title3>}, \enquote{<title4>}, \enquote{<title5>}.
name_parsing1 = <au>, \enquote{<title>} (<year>).
name_parsing2 = <au>, \enquote{<title>} (<year>).
name_parsing3 = <au>, \enquote{<title>} (<year>).
name_parsing4 = <au>, \textit{<title>} (<year>).
name_parsing5 = <au>, \textit{<title>} (<year>).
many_authors = <au>, \enquote{<title>} (<year>).
#many_editors = <ed.eds_message()>, \enquote{<title>} (<year>).
many_editors = <ed.if_singular(editorlist, option.edmsg1, option.edmsg2)>, \enquote{<title>} (<year>).
brace_delimited_quotes = <au>, \enquote{<title>} (<year>).
inproceedings = <au>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <eid> (<year>).
article = <au>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <eid> (<year>).
crossref1 = <au>, \enquote{<title>,} in \textit{<booktitle>}, <ed.if_singular(editorlist, option.edmsg1, option.edmsg2)>, Proc. SPIE \textbf{<volume>}: <eid> (<year>).
japanese = <au>, \enquote{<title-ja>,} <publisher-ja> (<year>). {\makeopenbracket}In <language>.{\makeclosebracket}
trailing_comma = <au>, \enquote{<title>} (<year>).
monthname1 = <au>, \enquote{<title>} (<month.monthname()>, <year>).
monthname2 = <au>, \enquote{<title>} (<month>, <year>).
monthabbrev = <au>, \enquote{<title>} (<month.monthabbrev()>, <year>).
replace_newlines = <au>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
quote_and_accent_detection = <au>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
hyperlinked_title = <au>, \enquote{[\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|],} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
edition_ordinal = <au>, \textit{<title>}[, <edition.ordinal()>~ed.][, vol.~<volume>] (<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
capitalized_field_names1 = <au>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
multilingual = <au>, \enquote{<title>} (<year>).
hindu = <au>, \enquote{<title>} (<year>).
user_defined_field = <au>, \enquote{<title>,} <group> (<year>).
movie1 = [<rating>]. \color{blue}{...
         <title>}\color{black}, <director> (\year>).
movie2 = [<rating>]. \color{blue}{<title>}\color{black}, <director> (\year>).
negativeyear = <au>, \enquote{<title>,} <institution> Tech.\ Rep.\ {\makehashsign}<number> (<year>).
use_sentence_case = <au>, \enquote{<title.sentence_case()>} (<year>).
malformed_template1 = <au> \enquote{<title.anycase()>} (<year>).
malformed_template2 = <au> \enquote{<title>} (<month|<year>).
malformed_template3 = <au> \enquote{<title>} (<month<year>).
malformed_template4 = <[<authorlist.0.first> ][<authorlist.0.middle.initial()>. ][<authorlist.0.prefix> ]<authorlist.0.last>[, <authorlist.0.suffix>]>
others_becomes_etal1 = <au> \enquote{<title>} (<year>).
others_becomes_etal2 = <au> \enquote{<title>} (<year>).
implicit_index = [<authorlist.0.first> ][<authorlist.0.middle.initial()>. ][<authorlist.0.prefix> ]<authorlist.0.last>[, <authorlist.0.suffix>]
french_initials = <au-A>, \enquote{<title>} (<year>).
use_name_ties = <au-B>, \enquote{<title>} (<year>).
period_after_initial = <au-C>, \enquote{<title>} (<year>).
terse_inits = <au-D>, \enquote{<title>} (<year>).
author_firstname_initials = <au-E>, \enquote{<title>} (<year>).
editor_firstname_initials = <ed-A.if_singular(editorlist, option.edmsg1, option.edmsg2)>, \enquote{<title>} (<year>).
andothers = \textit{<au-F>} <title> // <booktitle>[ / Ed. by <ed-B.if_singular(editorlist, option.nothing, option.etal_message)>] -- <publisher>, <address>, <year>. -- P.~<startpage> -- <endpage>.
lowerupper = <au>, <title.upper()> (<publisher.sentence_case()>, <address.lower()>, <year.upper()>).
substr_replace = <au.replace(J. W. Tukey,\textbf{J. W. Tukey})>, \enquote{<title.replace(Sunset,\color{red}Sunset\color{black})>,} <journal.replace(American,\textit{American})> \textbf{<volume>} (<year>).
japanese_name_separator = <au-G>, <title> (<year>).
zfill = <au.zfill()>, <title> (<year.zfill(4)>).
rangeindex = <au>, \enquote{<title.5:8>} (<year>).
author_or_editor1 = [[[<authorlist.0.first> ][<authorlist.0.prefix> ]<authorlist.0.last>]|[[<editorlist.0.first> ][<editorlist.0.prefix> ]<editorlist.0.last>]|No authors], \enquote{<title>} (<year>).
author_or_editor2 = [[[<authorlist.0.first> ][<authorlist.0.prefix> ]<authorlist.0.last>]|[[<editorlist.0.first> ][<editorlist.0.prefix> ]<editorlist.0.last>]|No editors], \enquote{<title>} (<year>).
author_or_editor3 = [[[<authorlist.0.first> ][<authorlist.0.prefix> ]<authorlist.0.last>]|[[<editorlist.0.first> ][<editorlist.0.prefix> ]<editorlist.0.last>]|No editors], \enquote{<title>} (<year>).
#name_abbrev1 = <au>, \enquote{<title>} (<year>).
#name_abbrev2 = <au>, \enquote{<title>} (<year>).
#if_length_equals1 = <emptystr.if_num_equals(authorlist.len(),3,au_three,au_two)> \textbf{<title>} (<year>).
#if_length_equals2 = <emptystr.if_num_equals(authorlist.len(),2,au_two,au_three)> \textbf{<title>} (<year>).
badkey = <au>
badtemplate = <badauthorname.0>
nofirstname = <au>, \enquote{<title>} (<year>).
any_namelist = <au> (<year>): <title>. In: <bau>/<ed>: <booktitle>.
bad_comma1 = <au>, \enquote{<title>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
bad_comma2 = <au>, \enquote{<title>} \textbf{<volume>}: <startpage>--<endpage> (<year>).


SPECIAL-TEMPLATES:
author = [<著者名>|<author-en>|]
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.first.initial()>. ][<authorlist.n.middle.initial()>. ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
au = <authorname.0>, ...,{ and }<authorname.9>
authorname-A.n = [<authorlist.n.first.frenchinitial()>. ][<authorlist.n.middle.frenchinitial()>. ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
au-A = <authorname-A.0>, ...,{ and }<authorname-A.N>
authorname-B.n = [<authorlist.n.first.initial()>.~][<authorlist.n.middle.initial().tie()>. ][<authorlist.n.prefix>~]<authorlist.n.last>[, <authorlist.n.suffix>]
au-B = <authorname-B.0>, ...,{ and }<authorname-B.N>
authorname-C.n = [<authorlist.n.first.initial()> ][<authorlist.n.middle.initial()> ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
au-C = <authorname-C.0>, ...,{ and }<authorname-C.N>
authorname-D.n = [<authorlist.n.first.initial()>][<authorlist.n.middle.initial().compress()> ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
au-D = <authorname-D.0>, ...,{ and }<authorname-D.N>
authorname-E.n = [<authorlist.n.first> ][<authorlist.n.middle> ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
au-E = <authorname-E.0>, ...,{ and }<authorname-E.N>
authorname-F.n = [<authorlist.n.prefix> ]<authorlist.n.last>, <authorlist.n.first.initial()>.[ <authorlist.n.middle.initial()>.][, <authorlist.n.suffix>.]
au-F = <authorname-F.0>, ..., <authorname-F.N>
authorname-G.n = <authorlist.n.first> <authorlist.n.last>
au-G = <authorname-G.0>, ..., <authorname-G.N>
badauthorname.n = [<authorlist.n.prefix> ]<authorlist.n.last>, <authorlist.n.first.initial()>.][ <authorlist.n.middle.initial()>.][, <authorlist.n.suffix>.]
editorname.n = [<editorlist.n.first.initial()>. ][<editorlist.n.middle.initial()>. ][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
ed = <editorname.0>, ...,{ and }<editorname.2>
editorname-A.n = [<editorlist.n.first> ][<editorlist.n.middle> ][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
ed-A = <editorname-A.0>, ...,{ and }<editorname-A.N>
editorname-B.n = [<editorlist.n.prefix> ]<editorlist.n.last>, <editorlist.n.first.initial()>.[ <editorlist.n.middle.initial()>.][, <editorlist.n.suffix>.]
ed-B = <editorname-B.0>
group = [<institution>|<organization>|<corporation>|]
citelabel = None
sortkey = <citenum.zfill(2)>
emptystr = {}
bookauthorlist = <bookauthor.to_namelist()>
bookauthorname.n = <bookauthorlist.n.last>[, <bookauthorlist.n.first>]
bau = <bookauthorname.0>/.../<bookauthorname.9>


OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
replace_newlines = True                   ## whether to remove newlines from the database entry fields
undefstr = ???                            ## what string to replace undefined required fields with
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs
etal_message = , \textit{et~al.}          ## what text to place at the end of an namelist when there are too many
edmsg1 = , ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present
nothing = {}                              ## the "if_singular()" operator need to print something, so here's an empty something
wrap_nested_quotes = True                 ## whether to replace \enquote{} commands and adjust nested quotations
autocomplete_doi = True                   ## whether to add "http://dx.doi.org/" to the front of the "doi" field if the front is missing.

#au_two = Two                              ## defined for use with the .if_length_equals() operator
#au_three = Three                          ## defined for use with the .if_length_equals() operator


VARIABLES:


DEFINITIONS:
