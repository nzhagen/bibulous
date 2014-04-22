TEMPLATES:
article = \textbf{<au>, (<year>[-<month.monthabbrev()>[-<day>]]):}\\ [\href{<url>}{<title>}|\href{<doi>}{<title>}|<title>|], \textit{<journal>} \textit{<volume>}([<number>|<issue>|]), [<startpage>--<endpage>|<startpage>|<eid>|].
book = \textbf{[<au>|<ed>|], (<year>[-<month.monthabbrev()>[-<day>]]):}\\ \textit{<title>}[, <edition_ordinal>~ed.][, <series>][ <issn>], <address>: <publisher>.

SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
authorname.n = [<authorlist.n.prefix> ]<authorlist.n.last>, <authorlist.n.first.initial()>.[ <authorlist.n.middle.initial()>.][, <authorlist.n.suffix>.]
au = <authorname.0>, ...{ \& }<authorname.9>
editorname.n = [<authorlist.n.prefix> ]<authorlist.n.last>, <authorlist.n.first.initial()>.[ <authorlist.n.middle.initial()>.][, <authorlist.n.suffix>.]
ed = <editorname.0>, ...{ \& }<editorname.5>
citelabel = <authorlist.0.last>-<year>
sortkey = <citelabel>

OPTIONS:
autocomplete_doi = True                   ## whether to add "http://dx.doi.org/" to the front of the "doi" field if the front is missing.
namelist_format = last_name_first
period_after_initial = True
use_firstname_initials = True
use_name_ties = False