TEMPLATES:
terse_inits = <authorliststr>, \enquote{<title>} (<year>).

OPTIONS:
terse_inits = True               ## whether to format initials as, for example, "DE" rather than "D. E."

SPECIAL-TEMPLATES:
authorname.n = [<authorlist.n.first.initial()>][<authorlist.n.middle.initial().compress()> ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
authorliststr = <authorname.0>, ...,{ and }<authorname.N>
editorname.n = [<editorlist.n.first.initial()>][<editorlist.n.middle.initial().compress()>][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
editorliststr = <editorname.0>, ...,{ and }<editorname.N>, eds
