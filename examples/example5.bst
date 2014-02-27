TEMPLATES:
article = \textbf{<au>:} \enquote{<title>}, in: \textit{<journal>} \textbf{<volume>} (<year>), <issue> [S.~<startpage>--<endpage>|S.~<startpage>|<eid>|] (<year>).[ <note>]
book = [\textbf{<au>:}|\textbf{<ed>} (Ed.) \textbf{:}|<organization>|<institution>|], \textit{<title>}[, <edition>~Aufl.][, (<series>; <number>)][, <address>] u.a.: <publisher> <year>.[ <note>]
inbook = \textbf{<au>:} \enquote{<title>}, in: [<ed.upper()> (Ed.): ]\textit{<booktitle>}[\textit{: <booksubtitle>}], <location> u.a.: <publisher> <year>, [S.~<startpage>--<endpage>|S.~<eid>|].[ <note>]

SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.first.initial()>.][, <authorlist.n.middle.initial()>.][, <authorlist.n.suffix>]
au = <authorname.0>; ...; <authorname.9>
editorname.n = [<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.first.initial()>.][, <editorlist.n.middle.initial()>.][, <editorlist.n.suffix>]
ed = <editorname.0>; ...; <editorname.2>
citelabel = <citenum>
sortkey = <authorlist.0.last>

OPTIONS:
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
edmsg1 = , ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present
name_separator = and                      ## the string used to separate names in a BibTeX-format field of names
wrap_nested_quotes = False                ## whether to attempt to match quotation levels within fields with a template formatting quotation marks
