TEMPLATES:
article = \textit{<au>} <title> // <journal> -- <year>. -- Vol.~<volume>. P.~[<startpage> -- <endpage>|<startpage>|<eid>|].
book = \textit{<au>} <title>. [Ch.~<chapter>. ]-- <address>: <publisher>, <year>.[ -- <startpage>~p.]
inbook = \textit{<au>} <title> // <booktitle>[ / Ed. by <ed.if_singular(editorlist, nothing, etal_message)>]. -- <address>: ...
         <publisher>, <year>.[ -- P.~<startpage> -- <endpage>| -- P.~<startpage>| -- P.~<eid>|].
inproceedings = \textit{<au>} <title> // <booktitle>[ / Ed. by <ed.if_singular(editorlist, nothing, etal_message)>]. -- ...
                <publisher>, <address>, <year>. -- P.~[<startpage> -- <endpage>|<startpage>|<eid>|].

SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.prefix> ]<authorlist.n.last>[ <authorlist.n.first.initial()>.][ <authorlist.n.middle.initial()>.][,  <authorlist.n.suffix>.]
au = <authorname.0>, ..., <authorname.9>
ed = [<editorlist.0.first.initial()>. ][ <editorlist.0.middle.initial()>. ][<editorlist.0.prefix> ]<editorlist.0.last>[,  <editorlist.0.suffix>.]

OPTIONS:
nothing = {}