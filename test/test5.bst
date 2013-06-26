TEMPLATES:
book = <authorliststr>, \textit{<title>} [\textit{<englishtitle>}] (<year_bce>). [In <language>.]
dialogue = <authorliststr>, \textit{<title>} [\textit{<englishtitle>}] (<year_bce>). [In <language>.]

OPTIONS:
use_firstname_initials = False            ## initialize all but the authors' last names
citation_order = ynt                      ## order the bibliography by "citekey" or "citenum" (or "nyt" etc.)
namelist_format = first_name_first        ## defines values for both "authorlist_format" and "editorlist_format" at once
yearstyle = 'BCE/CE'                      ## whether to use 'BCE/CE' after the year number or the older 'BC/AD' form

VARIABLES:
year_bce = format_yearstyle(entry['year'], options)
authorliststr = get_author(entry, options)

DEFINITIONS:
def format_yearstyle(yearstr, options):
    '''
    Append "BC or "AD" to "year", depending on whether the year is positive or negative.
    If the option "yearstyle" is set to "BCE/CE", then use "BCE" and "CE" instead of "BC"
    and "AD".
    '''

    ## First check that the input string is an integer.
    try:
        yearnum = int(yearstr)
    except ValueError:
        return(None)

    if (yearnum < 0):
        if (options['yearstyle'] == 'BCE/CE'):
            suffix = 'BC'
        else:
            suffix = 'BCE'
        result = str(yearnum) + ' ' + suffix
    elif (yearnum == 0):
        result = str(yearnum)
    else:
        if (options['yearstyle'] == 'BCE/CE'):
            suffix = 'CE'
        else:
            suffix = 'AD'
        result = str(yearnum) + ' ' + suffix

    return(result)

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
