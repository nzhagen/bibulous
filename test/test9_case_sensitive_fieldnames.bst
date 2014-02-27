TEMPLATES:
capitalized_field_names = <au>, \enquote{<TITLE>,} \textit{<JOURNAL>} \textbf{<VOLUME>}: <PAGES> (<YEAR>).


SPECIAL-TEMPLATES:
authorlist = <AUTHOR.to_namelist()>
editorlist = <EDITOR.to_namelist()>
au = <authorlist.format_authorlist()>
citelabel = None
sortkey = <citenum>


OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
sort_case = False                         ## whether to use case-sensitive citation sorting (default is False)
backrefs = False                          ## whether to implement backreferences in the bibliography -- maybe put in template strings?
backrefstyle = none                       ## can be one of {"none", "three", "two", "two+", "three+", "all+"}
hyperref = False                          ## whether to turn on (True) or off (False). If "hyperref" package is loaded, the default value is True, else default is False.
bibitemsep = 0pt                          ## the extra vertical separation between each bibliography entry. Defining this option *overrides* LaTeX's existing definition for \bibitemsep.
replace_newlines = True                   ## whether to remove newlines from the database entry fields
undefstr = ???                            ## what string to replace undefined required fields with
case_sensitive_field_names = True         ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs
etal_message = , \textit{et~al.}          ## what text to place at the end of an authorlist when there are too many
edmsg1 = , ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present
wrap_nested_quotes = False                ## whether to replace \enquote{} commands and adjust nested quotations


VARIABLES:


DEFINITIONS:
