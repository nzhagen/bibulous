TEMPLATES:
article = <au>, \enquote{[\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>],} <journal> \textbf{<volume>},{ }...
        [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).[ <note>]
book = [<au>|<ed>|<organization>|<institution>|], \textit{<title>}[, <edition.ordinal()>~ed.][, vol.~<volume>]{ }...
        (<publisher>, <year>)[ Chap.~<chapter>][, pp.~<startpage>--<endpage>|, p.~<startpage>].[ <note>]
electronic = [<au>, ] \enquote{<title>}\url{ [<url>|<doi>]}.
endnote = <note>
inbook = incollection
incollection = <au>, \enquote{<title>,} in \textit{<booktitle>}, [vol.~<volume>, ][<edition.ordinal()>~ed., ]...
        [<ed>, ][<series>, ][Chap.~<chapter>, ][pp.~<startpage>--<endpage>|p.~<startpage>|<eid>|] (<publisher>, <year>).[ <note>]
inproceedings = <au>, \enquote{<title>,} in \textit{<booktitle>}[, <ed>][, in <series>][ \textbf{<volume>}]...
        [, pp.~<startpage>--<endpage>|, p.~<startpage>|, <eid>] (<year>).[ <note>]
manual = [<au>|<ed>|<organization>|<institution>|], \textit{<title>}[, vol.~<volume>]...
        [, <edition.ordinal()>~ed.|, ver.~<version>][, <ed>] (<organization>, <year>)[, Chap.~<chapter>]...
        [, pp.~<startpage>--<endpage>|, p.~<startpage>].[ <note>]
mastersthesis = <au>, \enquote{<title>,} M.S. dissertation ([<school>|<institution>|], <year>).[ <note>]
misc = [<au>, ][\enquote{<title>}][ ([<organization>|<institution>|], <year>)| (<year>)].[ <note>][ (url: \url{<url>})]
note = <note>
patent = <au>, \enquote{<title>,} <nationality> patent <number> (<year>).[ <note>]
phdthesis = <au>, \enquote{<title>,} Ph.D. dissertation ([<school>|<institution>|], <year>).[ <note>]
poster = <au>, \enquote{<title>}, poster [presented at <conference>]([<month> ]<year>).[ <note>]
presentation = <au>, \enquote{<title>}, presentation [presented at <conference>]([<month> ]<year>).[ <note>]
proceedings = <ed>, \textit{<title>}, [vol.~<volume>][, <edition.ordinal()>~ed.] (<year>).[ <note>]
techreport = [<au>|<ed>|<organization>|<institution>|], \enquote{<title>,} <institution>, Tech. Rep. <number> (<year>).[ <note>]
website = \url{[<url>|<doi>]}
#website = \href{[<url>|<doi>]}{[<url>|<doi>]}

SPECIAL-TEMPLATES:
sortkey = <citenum.zfill(3)>              ## order the reference list in the same order as the citations were given in
citelabel = <citenum>                    ## use numeric reference labels

OPTIONS:
maxauthors = 25                           ## if more than 25 authors, then use "et al." format
minauthors = 9                            ## if "maxauthors" is exceeded, then display only the first "minauthors" and et al.
maxeditors = 5                            ## if more than 5 editors, then use "et al." format
mineditors = 5                            ## if "maxeditors" is exceeded, then display only the first "mineditors" and et al.
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
use_abbrevs = True                        ## whether to use the abbreviation strings (mainly useful for debugging)
french_initials = False                   ## whether to use French initials (i.e. Jean-Paul -> J.-P. and not J., also Philippe -> Ph. not P.)
etal_message = , \textit{et~al.}          ## what text to place at the end of an authorlist when there are too many
edmsg1 = , ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present

## The remaining exceptions below are really for users rather than for the journal.
undefstr = ???                            ## what string to replace undefined required fields with
replace_newlines = True                   ## whether to replace newline characters inside fields with spaces
allow_scripts = False                     ## whether to allow user scripts in BST files
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. so that "BOOK" will not be the same entrytype as "book")
use_citeextract = False                   ## whether to automatically perform citation extraction each time Bibulous is run
name_separator = and                      ## the string used to separate names in a BibTeX-format field of names

VARIABLES:

DEFINITIONS:
