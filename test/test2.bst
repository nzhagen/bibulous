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

SPECIAL-TEMPLATES:
authorname.n = [<authorlist.n.first.initial()>. ][<authorlist.n.middle.initial()>. ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
authorliststr = <authorname.0>, ...,{ and }<authorname.9>
editorname.n = [<editorlist.n.first.initial()>. ][<editorlist.n.middle.initial()>. ][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
editorliststr = <editorname.0>, ...,{ and }<editorname.2>, eds
citelabel = None
sortkey = <citenum>

OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
use_abbrevs = True                        ## whether to use the abbreviation strings (mainly useful for debugging)
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
undefstr = ???                            ## what string to replace undefined required fields with
replace_newlines = True                   ## whether to replace newline characters inside fields with spaces
case_sensitive_field_names = True         ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs
etal_message = , \textit{et al.}          ## what text to place at the end of an authorlist when there are too many


VARIABLES:

DEFINITIONS:
