TEMPLATES:
period_after_initial = <authorliststr>, \enquote{<title>} (<year>).

OPTIONS:
period_after_initial = False     ## whether to add a '.' after a person's initials.

SPECIAL-TEMPLATES:
authorname.n = [<authorlist.n.first.initial()> ][<authorlist.n.middle.initial()> ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
authorliststr = <authorname.0>, ...,{ and }<authorname.N>
editorname.n = [<editorlist.n.first.initial()> ][<editorlist.n.middle.initial()> ][<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
editorliststr = <editorname.0>, ...,{ and }<editorname.N>, eds

