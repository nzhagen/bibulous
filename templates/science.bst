TEMPLATES:
article = <au>, [<title>.] \textit{<journal>} \textbf{<volume>}, [<startpage>--<endpage>|<startpage>|<eid>|] (<year>)[, doi:<doi>].
book = [<au>|<ed>], \textit{<title>}[, <null.if_length_more_than(au,0,ed)>]{ }...
        (<publisher>, <address>[, ed.~<edition>], <year>)[, vol.~<volume>][ chap.~<chapter>][, pp.~<startpage>--<endpage>|, p.~<startpage>].
endnote = <note>
inbook = incollection
incollection = <au>, [\enquote{<title>,} ]in \textit{<booktitle>}[, <null.if_length_more_than(au,0,ed)>]{ }...
        (<publisher>, <address>[, ed.~<edition>], <year>)[, vol.~<volume>][ chap.~<chapter>][, pp.~<startpage>--<endpage>|, p.~<startpage>].
mastersthesis = <au>, thesis, <school> (<year>).
misc = [<au>, ][\enquote{<title>}][ (<organization>, <year>)| (<year>)].[ <note>][ (url: \url{<url>})]
phdthesis = <au>, thesis, <school> (<year>).
techreport = [<au>|<ed>|<organization>|<institution>], \enquote{<title>} ([Tech. Rep. <number>, ]<institution>, <address>, <year>).
website = [<title>, ]\url{[<url>|<doi>]}

#inproceedings = <au>, \enquote{<title>,} in \textit{<booktitle>}[, <ed>][, in <series>][ \textbf{<volume>}]...
#        [, pp.~<startpage>--<endpage>|, p.~<startpage>|, <eid>] (<year>).[ <note>]
#manual = [<au>|<ed>|<organization>|<institution>|], \textit{<title>}[, vol.~<volume>]...
#        [, <edition.ordinal()>~ed.|, ver.~<version>][, <ed>] (<organization>, <year>)[, Chap.~<chapter>]...
#        [, pp.~<startpage>--<endpage>|, p.~<startpage>].[ <note>]
#patent = <au>, \enquote{<title>,} <nationality> patent <number> (<year>).[ <note>]
#poster = <au>, \enquote{<title>}, poster [presented at <conference>]([<month> ]<year>).[ <note>]
#presentation = <au>, \enquote{<title>}, presentation [presented at <conference>]([<month> ]<year>).[ <note>]
#proceedings = <ed>, \textit{<title>}, [vol.~<volume>][, <edition.ordinal()>~ed.] (<year>).[ <note>]


SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.prefix> ]<authorlist.n.last>[ <authorlist.n.first.initial()>.][ <authorlist.n.middle.initial()>.][, <authorlist.n.suffix>.]
au = <authorname.0>, ..., <authorname.4>
editorname.n = [<editorlist.n.prefix> ]<editorlist.n.last>[ <editorlist.n.first.initial()>.][ <editorlist.n.middle.initial()>.][, <editorlist.n.suffix>.]
edz = <editorname.0>, ..., <editorname.4>
ed = <edz.if_singular(editorlist, edmsg1, edmsg2)>
citelabel = <citenum>.                    ## use numeric reference labels


OPTIONS:
etal_message = , \textit{et~al.}          ## what text to place at the end of an authorlist when there are too many
edmsg1 = , Ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , Eds.                           ## the label to use after the editor namelist when multiple editors are present
