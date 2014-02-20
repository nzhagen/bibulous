TEMPLATES:
article = <au> <year>. \textit{<journal>} \textbf{<volume>}:<pages>.
book = [<au>|<ed.if_singular(editorlist, eds_msg1, eds_msg2)>|]. <year>. \textit{<title>}. (<address>: <publisher>).
proceedings = book
phdthesis = <au> <year>. Ph.D. Thesis, <university>.


SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.first.initial()>.][ <authorlist.n.middle.initial()>.][,  <authorlist.n.suffix>.]
au = <authorname.0>, ...,{ and }<authorname.9>
editorname.n = [<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.first.initial()>.][ <editorlist.n.middle.initial()>.][,  <editorlist.n.suffix>.]
ed = <editorname.0>, ...,{ and }<editorname.5>
authorlabel = [<authorlist.0.prefix>|<authorlist.0.last>]
editorlabel = [<editorlist.0.prefix>|<editorlist.0.last>]
sortkey = [<authorlabel><year.zfill(4)>|<editorlabel><year>]
citelabel = (<citealnum>)


OPTIONS:
eds_msg1 = { }(ed.)
eds_msg2 = { }(eds.)
use_citeextract = True

