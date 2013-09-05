TEMPLATES:
book = <auth>, \textit{<title>} [\textit{<englishtitle>}] (<year_bce>). {\makeopenbracket}In <language>.{\makeclosebracket}
dialogue = <auth>, \textit{<title>} [\textit{<englishtitle>}] (<year_bce>). {\makeopenbracket}In <language>.{\makeclosebracket}
article = <auth>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>} (<number>), pp.~<pagerange> (<year>).
collection = [<for_japanese_audience><editor_ja>, <title_ja>, <volume>巻 (<publisher_ja> <address_ja> <year>).|...
              <for_english_audience><editorliststr>, <title_ja> (<title_romaji>) {\makeopenbracket}<title>{\makeclosebracket}, vol.~<volume> (<publisher>, <address>, <year>).|]


OPTIONS:
use_firstname_initials = False            ## initialize all but the authors' last names
citation_sort = ynt                       ## order the reference list by "citekey" or "citenum" (or "nyt" etc.)
citation_label = citenum                  ## label the reference items by their numerical order of appearance
namelist_format = first_name_first        ## defines values for both "authorlist_format" and "editorlist_format" at once
allow_scripts = True                      ## whether to allow user scripts in BST files
yearstyle = BCE/CE                        ## whether to use 'BCE/CE' after the year number or the older 'BC/AD' form
document_language = Japanese              ## whether the document is for a Japanese audience
use_citeextract = False                   ## turn off cite extraction, since this interferes with using multiple BIB file inputs

VARIABLES:
year_bce = format_yearstyle(entry['year'], options)
auth = get_author(entry, options)
pagerange = format_pagerange(entry, options)
for_japanese_audience = '{}' if (options['document_language'] == 'Japanese') else None
for_english_audience = '{}' if (options['document_language'] == 'English') else None


DEFINITIONS:
## NOTE! Only Unix-style line endings are allowed here.
def format_yearstyle(yearstr, options):
    '''
    Append "BC or "AD" to "year", depending on whether the year is positive or negative.
    If the option "yearstyle" is set to "BCE/CE", then use "BCE" and "CE" instead of "BC"
    and "AD".
    '''

    ## First check that the input string is an integer. If not an integer, then just return
    ## the field itself.
    if not str_is_integer(yearstr):
        return(yearstr)

    yearnum = int(yearstr)

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
def get_author(entry, options):
    '''
    In the test5 database, a given entry may have a "writer" field or an "author" field.
    Allow either one to be used in the same way. Note that this skips Bibulous' default
    reformatting of the list of authors. Here it is easy to do this since each author/writer
    is only one person, and so we can use the raw input.
    '''
    if ('author' in entry):
        return(entry['author'])
    elif ('writer' in entry):
        return(entry['writer'])
    else:
        return(options['undefstr'])

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
