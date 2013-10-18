TEMPLATES:
author_firstname_initials = <authorliststr>, \enquote{<title>} (<year>).
editor_firstname_initials = <editorliststr>, \enquote{<title>} (<year>).

OPTIONS:
use_firstname_initials = False      ## initialize all but the authors' last names

SPECIAL-TEMPLATES:
authorname.n = [<authorlist.n.first> ][<authorlist.n.middle> ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
authorliststr = <authorname.0>, ...,{ and }<authorname.N>
editorname.n = [<editorlist.n.first> ][<editorlist.n.middle> ][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
editorliststr = <editorname.0>, ...,{ and }<editorname.N>, eds

