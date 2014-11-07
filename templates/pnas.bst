TEMPLATES:
article = <au> (<year>) <title>. \textit{<journal>} <volume>(<number>): [<startpage>--<endpage>|<startpage>|<eid>|].[ <note>]
book = <au> (year>) \textit{<title>} (<publisher>, <address>)[, <edition.ordinal()>~Ed][, pp~<startpage>--<endpage>|, p~<startpage>].[ <note>]
incollection = <au> (<year>) <title>. \textit{<booktitle>}[, <edition_ordinal>~Ed][, <null.if_singular(editorlist, edmsg1, edmsg2)>~<ed>] (<publisher>, <address>)[, vol.~<volume>, ][, <series>][, Chap.~<chapter>][, pp~<startpage>--<endpage>|p~<startpage>|<eid>|].[ <note>]
database = <au> (<year>) <title>.[ Available at \url{<url>}[, accessed <access_date>].]
inproceedings = <au> (<year>) <title>. <booktitle>[, <null.if_singular(editorlist, edmsg1, edmsg2)>~<ed>] (<publisher>, <address>)[, pp~<startpage>--<endpage>|p~<startpage>|<eid>|].[ <note>]
techreport = <au> (<year>) <title>. Tech.\ Rep.\ <number> ([<institution>|<organization>|], <address>).[ <note>]
website = \url{[<url>|<doi>]}


SPECIAL-TEMPLATES:
citelabel = <citekey>
sortkey = <citekey>
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.prefix> ]<authorlist.n.last>[ <authorlist.n.first.initial()>][ <authorlist.n.middle.initial().compress()>][, <authorlist.n.suffix>]
au = <authorname.0>, ..., <authorname.9>
editorname.n = [<editorlist.n.prefix> ]<editorlist.n.last>[ <editorlist.n.first.initial()>][ <editorlist.n.middle.initial().compress()>][, <editorlist.n.suffix>]
ed = <editorname.0>, ..., <editorname.9>
null = {}


OPTIONS:
edmsg1 = ed
edmsg2 = eds
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.

## The remaining exceptions below are really for users rather than for the journal.
undefstr = ???                            ## what string to replace undefined required fields with
use_abbrevs = True                        ## whether to use the abbreviation strings (mainly useful for debugging)
replace_newlines = True                   ## whether to replace newline characters inside fields with spaces
allow_scripts = False                     ## whether to allow user scripts in BST files
case_sensitive_field_names = False        ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = True                    ## whether to automatically perform citation extraction each time Bibulous is run
etal_message = , \textit{et~al.}          ## what text to place at the end of a namelist when there are too many names
edmsg1 = , ed                             ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present
name_separator = and                      ## the string used to separate names in a BibTeX-format field of names
wrap_nested_quotes = False                 ## whether to replace \enquote{} commands and adjust nested quotations
autocomplete_doi = True                   ## whether to add "http://dx.doi.org/" to the front of the "doi" field if the front is missing.


VARIABLES:


DEFINITIONS:
