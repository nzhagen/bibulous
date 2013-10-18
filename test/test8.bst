TEMPLATES:
glossary = <description>
symbol = <description>
acronym = <description>

SPECIAL-TEMPLATES:
citelabel = <name>                      ## use "<name>" here since we want the acronym "name" field and not a name element
sortkey = <citekey>

OPTIONS:
citation_sort = citekey                 ## order the reference list by "citekey" or "citenum" (or "nyt" etc.)
citation_label = name                   ## the type of label to use for the reference list items
case_sensitive_field_names = True       ## whether to allow field names to be case sensitive (i.e. "BOOK" will not be the same entrytype as "book")
use_citeextract = False                 ## turn off cite extraction, since this interferes with using multiple BIB file inputs

