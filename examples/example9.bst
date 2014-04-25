TEMPLATES:
article = <au> (<year>). <title>. \textit{<journal>} \textit{<volume>}(<number>),{ }...
          [<startpage>--<endpage>|<startpage>|<eid>|].[ doi:\url{<doi>}| url:\url{<url>}]
newsarticle = <au> (<year>[, <month.monthname()>[ <day>]]). <title>. \textit{<journal>}. Retrieved <urldate>, from \url{<url>}.

SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
au = <authorlist.format_authorlist()>
ed = <editorlist.format_editorlist()>
citelabel = (<authorlist.0.last>, <year>)

OPTIONS:
namelist_format = last_name_first
