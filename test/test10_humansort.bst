TEMPLATES:
article = [<au>|<ed.if_singular(editorlist, option.edmsg1, option.edmsg2)>|], \enquote{<title>} (<year>).
incollection = [<au>|<ed.if_singular(editorlist, option.edmsg1, option.edmsg2)>|], \enquote{<title>,} <publisher> (<year>).[ {\makeopenbracket}In <language>.{\makeclosebracket}]

SPECIAL-TEMPLATES:
citelabel = -<citenum> test
sortkey = -<citenum> test