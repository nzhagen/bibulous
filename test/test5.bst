TEMPLATES:
book = <author>, \textit{<title>} [\textit{<englishtitle>}] (<year_bce>). {\makeopenbracket}In <language>.{\makeclosebracket}
dialogue = <author>, \textit{<title>} [\textit{<englishtitle>}] (<year_bce>). {\makeopenbracket}In <language>.{\makeclosebracket}
article = <author>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>} (<number>), pp.~<pagerange> (<year>).
collection = [<for_japanese_audience>[<author_ja>|<editor_ja>|], <title_ja>, <volume>巻 (<publisher_ja> <address_ja> <year>).|...
              <for_english_audience>[<author_en>|<editor_en>|], <title_ja> (<title_romaji>) {\makeopenbracket}<title_en>{\makeclosebracket}, vol.~<volume> (<publisher_en>, <address_en>, <year>).|]
本 = <著者名>, <題名> (<年>).


SPECIAL-TEMPLATES:
author = [<author_en>|<writer>|<著者名>]
editor = [<editor_en>]
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
citelabel = None
sortkey = <year.zfill(4)>[<authorlist.0.last>|<editorlist.0.last>|]<title>


OPTIONS:
allow_scripts = True                      ## whether to allow user scripts in BST files
yearstyle = BCE/CE                        ## whether to use 'BCE/CE' after the year number or the older 'BC/AD' form
document_language = Japanese              ## whether the document is for a Japanese audience
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs
etal_message = , \textit{et~al.}          ## what text to place at the end of an authorlist when there are too many
edmsg1 = , ed.                            ## the label to use after the editor namelist when only one editor is present
edmsg2 = , eds                            ## the label to use after the editor namelist when multiple editors are present
wrap_nested_quotes = False                ## whether to replace \enquote{} commands and adjust nested quotations


VARIABLES:
year_bce = format_yearstyle(entry, options)     ## format the year at append 'BC', 'AD', etc endings, depending on options settings
pagerange = format_pagerange(entry, options)
for_japanese_audience = '{}' if (options['document_language'] == 'Japanese') else None
for_english_audience = '{}' if (options['document_language'] == 'English') else None


DEFINITIONS:
## NOTE! Only Unix-style line endings are allowed here.
def format_yearstyle(entry, options):
    '''
    Append "BC or "AD" to "year", depending on whether the year is positive or negative.
    If the option "yearstyle" is set to "BCE/CE", then use "BCE" and "CE" instead of "BC"
    and "AD".
    '''

    if ('year' not in entry):
        #return(options['undefstr'])
        return(None)

    ## First check that the year string is an integer. If not an integer, then just return
    ## the field itself.
    if not str_is_integer(entry['year']):
        return(entry['year'])

    yearnum = int(entry['year'])

    if (yearnum < 0):
        if (options['yearstyle'] == 'BCE/CE'):
            suffix = 'BCE'
        else:
            suffix = 'BC'
        ## The "[1:]" here removes the minus sign.
        result = str(yearnum)[1:] + ' ' + suffix
    elif (yearnum == 0):
        result = str(yearnum)
    else:
        if (options['yearstyle'] == 'BCE/CE'):
            suffix = 'CE'
        else:
            suffix = 'AD'
        result = str(yearnum) + ' ' + suffix

    return(result)

## ==================================
def format_pagerange(entry, options):
    '''
    If the "pages" field is comma-delimited, then return the pages field as-is. Otherwise
    return the standard startpage--endpage range.
    '''

    if not ('pages' in entry):
        return(None)
    elif (',' in entry['pages']):
        return(entry['pages'])
    else:
        return(entry['startpage']--entry['endpage'])
