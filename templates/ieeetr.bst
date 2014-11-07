TEMPLATES:
article = <au>, \enquote{<title>,} \textit{<journal>} vol.~<volume>: [pp.~<startpage>--<endpage>|p.~<startpage>|<eid>|], [<month.monthabbrev()> ]<year>.[ <note>]
book = [<au>|<ed.if_singular(editorlist, edmsg1, edmsg2)>|<organization>|<institution>|], \textit{<title>}[, vol.~<volume>]. [<address>: ]<publisher>, [<edition.ordinal()>~ed., ][<month.monthabbrev()> ]<year>.[ <note>]
booklet = <au>, \enquote{<title>.} [<howpublished>, ][<address>, ][<month.monthabbrev()> ]<year>.[ <note>]
conference = [<au>|<organization>|<institution>|], \enquote{<title>,} [in \textit{<booktitle>}][ (<ed.if_singular(editorlist, edmsg1, edmsg2)>), ][vol.~<volume>, ] (<address>)[, p.~<startpage>][, <organization>], <publisher>, [<month.monthabbrev()> ]<year>.[ <note>]
inbook = <au>, \textit{<title>}, [vol.~<volume>, ][ch.~<chapter>, ][pp.~<startpage>--<endpage>|<eid>|]. <address>: <publisher>, [<edition.ordinal()>~ed., ][<month.monthabbrev()> ]<year>).[ <note>]
incollection = [<au>|<organization>|<institution>|], \enquote{<title>,} [in \textit{<booktitle>}][ (<ed.if_singular(editorlist, edmsg1, edmsg2)>), ][vol.~<volume>, ][ch.~<chapter>, ][pp.~<startpage>--<endpage>|<eid>|] <address>: <publisher>, [<edition.ordinal()>~ed., ][<month.monthabbrev()> ]<year>.[ <note>]
manual = [<au>|<ed.if_singular(editorlist, edmsg1, edmsg2)>|], \textit{<title>}. [<organization>, ][<address>, ][<edition.ordinal()>~ed., |ver.~<version>, ][<month.monthabbrev()> ]<year>).[ <note>]
mastersthesis = <au>, ``<title>,'' Master's thesis, <school>, <address>, [<month.monthabbrev()> ]<year>).[ <note>]
misc = <au>, \enquote{<title>.}[ <howpublished>, ]<month.monthabbrev()> ]<year>.[ <note>]
phdthesis = <au>, \textit{<title>}, Ph.D. thesis, <school>, <address>, [<monthrname> ]<year>.[ <note>]
proceedings = <ed.if_singular(editorlist, edmsg1, edmsg2)>, ed., \textit{<title>}, [vol.~<volume>, ][<organization>, ]<publisher> [<month.monthabbrev()> ]<year>.[ <note>]
techreport = <au>, \enquote{<title>,} Tech.\ Rep.\ <number>, [<institution>, |<organization>, |]<publisher>, [<month.monthabbrev()> ]<year>.[ <note>]
unpublished = <au>, \enquote{<title>.}[ <note>,] [<month.monthabbrev()> ]<year>.
website = \url{[<url>|<doi>]}


SPECIAL-TEMPLATES:
sortkey = <citenum>                       ## order the reference list in the same order as the citations were given in
citelabel = <citenum.remove_leading_zeros()>  ## use numeric reference labels


OPTIONS:
maxauthors = 9                            ## if more than 10 authors, then use "et al." format
minauthors = 9                            ## if "maxauthors" exceeded, then display only the first "minauthors" and et al.
maxeditors = 5                            ## if more than 5 editors, then use "et al." format
mineditors = 5                            ## if "maxeditors" exceeded, then display only the first "mineditors" and et al.
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
use_abbrevs = True                        ## whether to use the abbreviation strings (mainly useful for debugging)
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
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

