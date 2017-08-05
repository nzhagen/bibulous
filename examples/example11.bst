article       = {\sc <au>}, \enquote{<title>,} \textit{<journal>,} [\textbf{<volume>}][:<number>] [<startpage>-<endpage>|<startpage>] ([<month>[ <day>], ]<year>).

SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
authorname.n = <authorlist.n.last>[, <authorlist.n.first.initial()>.][ <authorlist.n.middle.initial()>.][,  <authorlist.n.suffix>.]
au = <authorname.0>, ...,{ and }<authorname.5>
authorlast.n = <authorlist.n.last>
authorlabel = [<authorlist.0.prefix>|<authorlist.0.last>]
sortkey = [<authorlist.0.last><year>]
citelabel = [{<authorlast.0>, ...{ and }<authorlast.1>}(<year>){<au>}]

OPTIONS:
eds_msg1        = { } ed.
eds_msg2        = { } eds.
use_citeextract = False

