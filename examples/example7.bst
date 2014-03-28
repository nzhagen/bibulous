TEMPLATES:
article = <au>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>},{ }...
          [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).
book = <au>, \textit{<title>} (<publisher>, <year>).
incollection = <au>, \enquote{<title>,} in \textit{<booktitle>}, [Chap.~<chapter>, ]...
        [pp.~<startpage>--<endpage>|p.~<startpage>|<eid>|] (<publisher>, <year>).
mastersthesis = <au>, \enquote{<title>,} M.S. dissertation (<school>, <year>).
phdthesis = <au>, \enquote{<title>,} Ph.D. dissertation (<school>, <year>).

SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
au = <authorlist.format_authorlist()>
ed = <editorlist.format_editorlist()>

OPTIONS:
allow_scripts = True         ## whether to allow user scripts in BST files

VARIABLES:
citelabel = create_citelabel(entry, options)

DEFINITIONS:
def create_citelabel(entry, options):
    numnames = len(entry['authorlist'])
    if (numnames == 0): return(entry['citenum'])
    foundit = False
    for name in entry['authorlist']:
        if (name['last'] == 'Broglie') and (name['prefix'] == 'de'):
            foundit = True
            break
    if foundit:
        return(r'\textbf{' + entry['citenum'] + '}')
    else:
        return(entry['citenum'])
