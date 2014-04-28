TEMPLATES:
article = <au>, ``[\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|],'' \textit{<journal>} \textbf{<volume>}: [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).[ <note>]
book = [<au>|<ed>|<organization>|<institution>|], \textit{<title>}[, <edition_ordinal>~ed.][, vol.~<volume>] (<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
booklet = [<au>|<ed>|<organization>|<institution>|], \textit{<title>}, [vol.~<volume>, ][<edition_ordinal>~ed., |ver.~<version>, ][<ed>, ] (<organization>, <year>)[, Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
endnote = <note>
inbook = incollection
incollection = <au>, ``<title>,'' in \textit{<booktitle>}, [vol.~<volume>, ][<edition_ordinal>~ed., ][<ed>, ][<series>, ][Chap.~<chapter>, ][pp.~<startpage>--<endpage>|<eid>|] (<publisher>, <year>).[ <note>]
inproceedings = <au>, ``<title>,'' in \textit{<booktitle>}[, <ed>][, in <series>][ \textbf{<volume>}][, pp.~<startpage>--<endpage>|, <eid>] (<year>). [<note>]
manual = [<au>|<ed>|<organization>|<institution>|], \textit{<title>}, [vol.~<volume>, ][<edition_ordinal>~ed., |ver.~<version>, ][<ed>, ] (<organization>, <year>)[, Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
mastersthesis = <au>, ``<title>,'' M.S. dissertation (<school>, <year>).[ <note>]
misc = [<au>, ][``<title>''][ (<organization>, <year>)| (<year>)].[ <note>]
patent = <au>, ``<title>,'' <nationality> patent <number> (<year>).[ <note>]
phdthesis = <au>, ``<title>,'' Ph.D. dissertation (<school>, <year>).[ <note>]
proceedings = <ed>, \textit{<title>}, [vol.~<volume>][, <edition_ordinal>~ed.] (<year>).[ <note>]
techreport = [<au>, |<ed>, ]``<title>,'' <institution>, Tech.\ Report <number> (<year>).[ <note>]
unpublished = misc


SPECIAL-TEMPLATES:
##sortkey = [<authorlist.0.last>|<editorlist.0.last>|<organization>]<year><title>
##sortkey = <author>
##citelabel = [<authorlist.0.last>|<editorlist.0.last>|<organization>|]<year>


OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
replace_newlines = True                   ## whether to replace newline characters inside fields with spaces
case_sensitive_field_names = True         ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs
etal_message = , \textit{et~al.}          ## what text to place at the end of an authorlist when there are too many
edmsg1 = , ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present


VARIABLES:

DEFINITIONS:
