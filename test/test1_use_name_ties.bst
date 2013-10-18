TEMPLATES:
use_name_ties = <authorliststr>, \enquote{<title>} (<year>).

OPTIONS:
use_name_ties = True             ## whether to use ties ('~') instead of spaces to glue together initials.

SPECIAL-TEMPLATES:
authorname.n = [<authorlist.n.first.initial()>.~][<authorlist.n.middle.initial().tie()>. ][<authorlist.n.prefix>~]<authorlist.n.last>[, <authorlist.n.suffix>]
authorliststr = <authorname.0>, ...,{ and }<authorname.N>
editorname.n = [<editorlist.n.first.initial()>~.][<editorlist.n.middle.initial().tie()>. ][<editorlist.n.prefix>~]<editorlist.n.last>[, <editorlist.n.suffix>]
editorliststr = <editorname.0>, ...,{ and }<editorname.N>, eds
