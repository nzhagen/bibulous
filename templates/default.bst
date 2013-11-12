TEMPLATES:
article = <au>, \enquote{[\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|],} \textit{<journal>} \textbf{<volume>}: [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).[ <note>]
book = [<au>|<ed.eds_message()>|<organization>|<institution>|], \textit{<title>}[, <edition.ordinal()>~ed.][, vol.~<volume>] (<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
endnote = <note>
inbook = incollection
incollection = <au>, \enquote{<title>,} in \textit{<booktitle>}, [vol.~<volume>, ][<edition.ordinal()>~ed., ][<ed.eds_message()>, ][<series>, ][Chap.~<chapter>, ][pp.~<startpage>--<endpage>|<eid>|] (<publisher>, <year>).[ <note>]
inproceedings = <au>, \enquote{<title>,} in \textit{<booktitle>}[, <ed.eds_message()>][, in <series>][ \textbf{<volume>}][, pp.~<startpage>--<endpage>|, <eid>] (<year>). [<note>]
manual = [<au>|<ed.eds_message()>|<organization>|<institution>|], \textit{<title>}, [vol.~<volume>, ][<edition.ordinal()>~ed., |ver.~<version>, ][\comment{<au>}|<ed.eds_message()>, ] (<organization>, <year>)[, Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
mastersthesis = <au>, \enquote{<title>,} M.S. dissertation (<school>, <year>).[ <note>]
misc = [<au>, ][\enquote{<title>}][ (<organization>, <year>)| (<year>)].[ <note>]
patent = <au>, \enquote{<title>,} <nationality> patent <number> (<year>).[ <note>]
phdthesis = <au>, \enquote{<title>,} Ph.D. dissertation (<school>, <year>).[ <note>]
proceedings = <ed.eds_message()>, \textit{<title>}, [vol.~<volume>][, <edition.ordinal()>~ed.] (<year>).[ <note>]
techreport = [<au>, |<ed.eds_message()>, ]``<title>,'' <institution>, Tech.\ Report <number> (<year>).[ <note>]
##article = <au>, \enquote{\href{[<url>|<doi>]}{<title>},} <journal> \textbf{<volume>}, [<startpage>--<endpage>|<eid>|] (<year>).[ <note>][ {\makeopenbracket}<url>{\makeclosebracket}| {\makeopenbracket}<doi>{\makeclosebracket}]
##book = [<au>|], \textit{<title>}, [<edition.ordinal()>~ed., ][vol.~<volume>, ](<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>].[ <note>]
##inproceedings = <au>, \enquote{<title>,} [in \textit{<booktitle>}, <ed.eds_message()>, <series> |in \textit{<booktitle>}, <series> |in \textit{<booktitle>}, ]\textbf{<volume>}[, pp.~<startpage>--<endpage>|, <eid>] (<year>).[ <note>]

SPECIAL-TEMPLATES:
sortkey = <citekey>                       ## order the reference list by "citekey"
citelabel = <citekey>                     ## the type of label to use for the reference list items

OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
use_abbrevs = True                        ## whether to use the abbreviation strings (mainly useful for debugging)
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
month_abbrev = True                       ## whether to use abbreviated month names (i.e. "Jan" instead of "January").
eds_message = {, ed.}{, eds}              ## the label to use after the editor namelist (first braces for one editor, second braces for multiple editors)

## The remaining exceptions below are really for users rather than for the journal. Maybe put these someplace else?
undefstr = ???                            ## what string to replace undefined required fields with
replace_newlines = True                   ## whether to replace newline characters inside fields with spaces
allow_scripts = False                     ## whether to allow user scripts in BST files
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")

VARIABLES:

DEFINITIONS:

