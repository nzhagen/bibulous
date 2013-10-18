TEMPLATES:
french_initials = <authorliststr>, \enquote{<title>} (<year>).

OPTIONS:
french_initials = True           ## whether to use French initials (i.e. Jean-Paul -> J.-P. and not J., also Philippe -> Ph. not P.)

SPECIAL-TEMPLATES:
authorname.n = [<authorlist.n.first.frenchinitial()>. ][<authorlist.n.middle.frenchinitial()>. ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
authorliststr = <authorname.0>, ...,{ and }<authorname.N>
editorname.n = [<editorlist.n.first.frenchinitial()>. ][<editorlist.n.middle.frenchinitial()>. ][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
editorliststr = <editorname.0>, ...,{ and }<editorname.N>, eds
