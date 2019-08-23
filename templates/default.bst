TEMPLATES:
article = <au>, \enquote{[\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|],} \textit{<journal>} \textbf{<volume>}: [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).[ <note>]
book = [<au>|<ed.if_singular(editorlist, edmsg1, edmsg2)>|<organization>|<institution>|], \textit{<title>}[, <edition.ordinal()>~ed.][, vol.~<volume>] (<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
electronic = [<au>, ] \enquote{<title>}\url{ [<url>|<doi>]}.
endnote = <note>
inbook = incollection
incollection = <au>, \enquote{<title>,} in \textit{<booktitle>}, [vol.~<volume>, ][<edition.ordinal()>~ed., ][<ed.if_singular(editorlist, edmsg1, edmsg2)>, ][<series>, ][Chap.~<chapter>, ][pp.~<startpage>--<endpage>|<eid>|] (<publisher>, <year>).[ <note>]
inproceedings = <au>, \enquote{<title>,} in \textit{<booktitle>}[, <ed.if_singular(editorlist, edmsg1, edmsg2)>][, in <series>][ \textbf{<volume>}][, pp.~<startpage>--<endpage>|, <eid>] (<year>). [<note>]
manual = [<au>|<ed.if_singular(editorlist, edmsg1, edmsg2)>|<organization>|<institution>|], \textit{<title>}, [vol.~<volume>, ][<edition.ordinal()>~ed., |ver.~<version>, ][\comment{<au>}|<ed.if_singular(editorlist, edmsg1, edmsg2)>, ] (<organization>, <year>)[, Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
mastersthesis = <au>, \enquote{<title>,} M.S. dissertation (<school>, <year>).[ <note>]
misc = [<au>, ][\enquote{<title>}][ (<organization>, <year>)| (<year>)].[ <note>]
patent = <au>, \enquote{<title>,} <nationality> patent <number> (<year>).[ <note>]
phdthesis = <au>, \enquote{<title>,} Ph.D. dissertation (<school>, <year>).[ <note>]
proceedings = <ed.if_singular(editorlist, edmsg1, edmsg2)>, \textit{<title>}, [vol.~<volume>][, <edition.ordinal()>~ed.] (<year>).[ <note>]
techreport = [<au>, |<ed.if_singular(editorlist, edmsg1, edmsg2)>, ]``<title>,'' <institution>, Tech.\ Report <number> (<year>).[ <note>]
website = \url{[<url>|<doi>]}
##article = <au>, \enquote{\href{[<url>|<doi>]}{<title>},} <journal> \textbf{<volume>}, [<startpage>--<endpage>|<eid>|] (<year>).[ <note>][ {\makeopenbracket}<url>{\makeclosebracket}| {\makeopenbracket}<doi>{\makeclosebracket}]
##book = [<au>|], \textit{<title>}, [<edition.ordinal()>~ed., ][vol.~<volume>, ](<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
##inproceedings = <au>, \enquote{<title>,} [in \textit{<booktitle>}, <ed.if_singular(editorlist, edmsg1, edmsg2)>, <series> |in \textit{<booktitle>}, <series> |in \textit{<booktitle>}, ]\textbf{<volume>}[, pp.~<startpage>--<endpage>|, <eid>] (<year>).[ <note>]


SPECIAL-TEMPLATES:
sortkey = <citekey>                       ## order the reference list by "citekey"
citelabel = <citekey>                     ## the type of label to use for the reference list items


OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
use_abbrevs = True                        ## whether to use the abbreviation strings (mainly useful for debugging)
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
month_abbrev = True                       ## whether to use abbreviated month names (i.e. "Jan" instead of "January").
etal_message = , \textit{et~al.}          ## what text to place at the end of an authorlist when there are too many
edmsg1 = , ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present

## The remaining exceptions below are really for users rather than for the journal.
undefstr = ???                            ## what string to replace undefined required fields with
replace_newlines = True                   ## whether to replace newline characters inside fields with spaces
allow_scripts = False                     ## whether to allow user scripts in BST files
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
name_separator = and                      ## the string used to separate names in a BibTeX-format field of names


VARIABLES:


DEFINITIONS:

