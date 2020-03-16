TEMPLATES:
article = <au> <year> <title> \textit{<journal>} [\href{<url>}{\textbf{<volume>} <refpages>}|\href{<doi>}{\textbf{<volume>} <refpages>}|\textbf{<volume>} <refpages>|][ <note>]
book = [<au>|<ed>|] <year> \textit{<title>}[ <edition.ordinal()>~edn][ <series>] ([<address>: ]<publisher>)[ <note>]
inbook = <au> <year> <title> in \textit{<booktitle>} [ <edition.ordinal()>~edn][ <series>][ ed <ed>] ([<address>: ]<publisher>)[ Chap.\ <chapter>][ pp <startpage>--<endpage>|p <startpage>|<eid>|][ <note>]
incollection = <au> <year> [\href{<doi>}{<title>}|\href{<url>}{<title>}|<title>|] in \textit{<booktitle>} [ <edition.ordinal()>~edn][ <series>][ ed <ed>] ([<address>: ]<publisher>)[ Chap.\ <chapter>][ pp <startpage>--<endpage>|p <startpage>|<eid>|][ <note>]
inproceedings = <au> <year> [\href{<doi>}{<title>}|\href{<url>}{<title>}|<title>|] \textit{<booktitle>}[ <series>][ pp <startpage>--<endpage>|p <startpage>|<eid>][ <note>]
misc = <au> <year> [\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|][ <note>]
phdthesis = <au> <year> <title> Ph.D. dissertation (<school>).[ <note>]
presentation = <au> <year> [\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|][ <note>]
techreport = [<au>|<ed>|<organization>|<institution>|] <year> <title>[ Tech.\ Rep.~<number>][ <au.exists()><institution>|<ed.exists()><institution>][ (<address>)][ <note>]
website = [\href{<url>}{<title>}|\href{<doi>}{<title>}|][ Accessed: <date>]


SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.prefix> ]<authorlist.n.last> <authorlist.n.first.initial()>[ <authorlist.n.middle.initial()>][, <authorlist.n.suffix>]
au = <authorname.0>, ...{ and }<authorname.9>
editorname.n = [<authorlist.n.prefix> ]<authorlist.n.last> <authorlist.n.first.initial()>[ <authorlist.n.middle.initial()>][, <authorlist.n.suffix>]
ed = <editorname.0>, ...{ and }<editorname.5>
refpages = [<startpage>--<endpage>|<startpage>|<eid>|]


OPTIONS:
procspie_as_journal = True                ## treat SPIE conference proceedings like a journal, with journal name 'Proc. SPIE'
autocomplete_url = True
