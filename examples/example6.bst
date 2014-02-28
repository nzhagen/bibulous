TEMPLATES:
article = <au>[ (<nameaddon>)], \enquote{<title>}. In: \textit{<journal>} <volume> (<year>), [pp.~<startpage>--<endpage>|p.~<startpage>|<eid>|].[ <note>]

SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.first> ][<authorlist.n.middle> ][<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
au = <authorname.0>; ...; <authorname.9>
citelabel = [<shortauthor.0:2><year.2:3>|<authorlist.0.last.0:2><year.2:3>|]
sortkey = <authorlist.0.last>
