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
#name_abbrev1 = <authorliststr>, \enquote{<title>} (<year>).
#name_abbrev2 = <authorliststr>, \enquote{<title>} (<year>).
brace_delimited_quotes = <authorliststr>, \enquote{<title>} (<year>).
inproceedings = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <eid> (<year>).
article = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <eid> (<year>).
crossref1 = <authorliststr>, \enquote{<title>,} in \textit{<booktitle>}, <editorliststr>, Proc. SPIE \textbf{<volume>}: <eid> (<year>).
japanese = <authorliststr>, \enquote{<title-ja>,} <publisher-ja> (<year>). {\makeopenbracket}In <language>.{\makeclosebracket}
trailing_comma = <authorliststr>, \enquote{<title>} (<year>).
monthformat1 = <authorliststr>, \enquote{<title>} (<monthname>, <year>).
monthformat2 = <authorliststr>, \enquote{<title>} (<monthname>, <year>).
monthformat3 = <authorliststr>, \enquote{<title>} (<month>, <year>).
replace_newlines = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
quote_and_accent_detection = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
hyperlinked_title = <authorliststr>, \enquote{[\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|],} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
edition_ordinal = <authorliststr>, \textit{<title>}[, <edition_ordinal>~ed.][, vol.~<volume>] (<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
capitalized_field_names1 = <authorliststr>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: <startpage>--<endpage> (<year>).
multilingual = <authorliststr>, \enquote{<title>} (<year>).
hindu = <authorliststr>, \enquote{<title>} (<year>).
user_defined_field = <authorliststr>, \enquote{<title>,} <group> (<year>).
movie1 = [<rating>]. \color{blue}{...
         <title>}\color{black}, <director> (\year>).
movie2 = [<rating>]. \color{blue}{<title>}\color{black}, <director> (\year>).
negativeyear = <authorliststr>, \enquote{<title>,} <institution> Tech.\ Rep.\ {\makehashsign}<number> (<year>).
#use_sentence_case = <authorliststr>, \enquote{<title.sentence_case()>} (<year>).


SPECIAL-TEMPLATES:
author = [<著者名>|<author-en>|]
authorname.n = [<authorlist.n.first.initial()>. ][<authorlist.n.middle.initial()>. ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
authorliststr = <authorname.0>, ...,{ and }<authorname.9>
editorname.n = [<editorlist.n.first.initial()>. ][<editorlist.n.middle.initial()>. ][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
editorliststr = <editorname.0>, ...,{ and }<editorname.2>, eds
group = [<institution>|<organization>|<corporation>|]
citelabel = None
sortkey = <citenum>


OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
month_abbrev = True                       ## whether to use abbreviated month names (i.e. "Jan" instead of "January").
replace_newlines = True                   ## whether to remove newlines from the database entry fields
undefstr = ???                            ## what string to replace undefined required fields with
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs
etal_message = , \textit{et al.}          ## what text to place at the end of an authorlist when there are too many


VARIABLES:

DEFINITIONS:
