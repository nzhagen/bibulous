Guidelines for writing bibliography style templates
===================================================

Syntax
------

#. Comments begin with ``#``, following the Python convention.

#. Each template file can have as many as five sections. None of the sections are required to be in the file, but any definitions in the file must be placed inside a section header so that the code knows how to deal with the definition. The four possible section headers are: TEMPLATES, SPECIAL-TEMPLATES, OPTIONS, VARIABLES, DEFINITIONS. And note that a section header is always placed by itself on a line and has a colon appended to it, as in ``TEMPLATES:``.

#. All variable definitions use the variable name followed by whitespace, an equals sign, more whitespace, and then the definition itself. Thus the whitespace+=+whitespace is the delimiter between variable and definition, and is required syntax.

#. Inside the ``TEMPLATES`` section, all of the variable definitions are intended to map to a database entrytype name. For example::

      article = <au>, ``<title>,'' <journal>, <volume>, <startpage>--<endpage> (<year>).

   Here the ``article`` entrytype will be typeset so that the list of authors (``<au>``) is followed by the article title in double quotes, the journal name in standard font (i.e. not italics), the volume number, the page range, and the year.

#. A variable is indicated by angle brackets, as ``<var>`` and represents the contents of a field found within the bibliography database. Thus, when typesetting the bibliography, Bibulous will replace the variable ``<authorlist>`` with the string stored in the ``authorlist`` field of the current entry being formatted. An example list of typical variables one might use is:

      ``<au>``, ``<booktitle>``, ``<chapter>``, ``<edition>``, ``<ed>``, ``<eid>``, ``<endpage>``, ``<institution>``, ``<journal>``, ``<nationality>``, ``<note>``, ``<number>``, ``<organization>``, ``<publisher>``, ``<school>``, ``<series>``, ``<startpage>``, ``<title>``, ``<version>``, ``<volume>``, ``<year>``.

   This list is actually freely extensible. A user can add any additional variables needed, so that if a ``video`` field is used in a ``.bib`` database file, then this can be used within a formatted reference simply by placing ``<video>`` into the template wherever the information needs to be inserted.

#. Any variable placed within square brackets ``[]`` indicate that it is an optional variable --- it is not required that the database have that entry. While required entries that are not defined in the BibTeX database file (.bib file) are replaced with '???', and undefined optional variables are simply skipped. If a ``|`` is present within the square brackets, it indicates an "elseif" clause. That is, if the template is ``[<var1>|<var2> and <var3>]``, then the code will look for ``var1`` as a field within the current database entry being formatted. If it does not find the entry, then it will try the next block, where it finds the two variables ``var2`` and ``var3``. If both are defined, then the original template ``[<var1>|<var2> and <var3>]`` is replaced with ``<var2> and <var3>`` (i.e. removing the square brackets) and proceeds to replace the two variables with their corresponding fields. If either one of ``var2`` or ``var3`` is undefined in the entry, then the entire optional [...] portion of the template is skipped.

#. If the ``|`` symbol is used to create an empty last cell, as in ``[<var1>|<var2>|]``, this indicates that while the individual cells within the optional block are themselves optional, it is required to have at least _one_ among the cells to be defined. Thus, ``[<note>|]`` has the same meaning as simply ``<note>`` does.

#. Nesting of ``[]`` brackets is allowed, but the syntax becomes computationally expensive to parse, so that these structures should be used sparingly::

#. Users that need to use ``[``, ``]``, ``#``, ``<``, ``>``, or ``|`` symbols as formatting elements within the reference list can implement them using some custom LaTeX-markup commands: ``{\makeopenbracket}``, ``{\makehashsign}``, ``{\makeclosebracket}``, ``{\makegreaterthan}``, ``{\makelessthan}``, or ``{\makeverticalbar}``. Note that the curly brackets used in each case are required.

#. In the ``TEMPLATES`` section of the file, if an entrytype format definition contains only another entrytype name on the right hand side of the ``=``, i.e.::

       inbook = incollection

   then this means that the existing ``incollection`` template should be copied for use with ``inbook`` entrytypes. (Note that ``incollection`` should be defined above this line in order for this to work.)

#. Note that several fields are defined by default which are *not* directly from the bibliography database. These are ``au``, ``authorlist``, ``citekey``, ``citenum``, ``ed``, ``editorlist``, ``endpage``, and ``startpage``. These fields are derived from the original database file, but have been reformatted. See the *Default Fields* section below.

#. Although the entrytype template definitions listed below are in alphabetical order, that can be put in any desired order within the file. (The exception to this rule is that if a definition consists of, for example::

      inbook = incollection

   then the ``incollection`` template must already be defined. Also note that two entrytype names are special and so cannot be used on the left hand side of the equals sign here: ``comment`` and ``preamble``.

#. A user wanting a localized form of quotation should use ``\enquote{<title>}`` rather than ````<title>''``, and add ``\usepackage{csquotes}`` to the preamble of the LaTeX document.

#. In the ``OPTIONS`` section of the file are the formatting options. None of these definitions are required. The complete list is given in the *Options keywords* section below, together with explanations of each.

#. The ``SPECIAL-TEMPLATES`` section is where users can define their own fields that get generated for every database entry evaluated. For example, the variable definition::

    group = [<organization>|<institution>|<corporation>|]

    in the ``SPECIAL-TEMPLATES`` section will create a ``group`` field that can be used as the variable ``<group>`` within the regular ``TEMPLATES`` section of the file. This effectively allows users to create a shortcut. Where they could write out ``[<organization>|<institution>|<corporation>|]`` inside each template that needs this structure, the special template definition allows them to replace each instance with a simple ``<group>``.

#. The order in which any definitions are placed within the special templates is important. For example, if a user has ``au = <authorlist.format_authorlist()>`` and then below that defines ``authorlist = <author.to_namelist()>``, then the code will issue an error stating that ``authorlist`` is not defined when attempting to create the ``au`` variable. Since the definition for ``au`` assumes the presence of the ``authorlist`` variable, the latter definition must be placed above it.

#. [ADD MORE DETAILS HERE ON NEWER CODE STRUCTURES, such as implicit indexing and implicit loops. What else to go here?]

Default Fields
--------------

A complete of the existing default fields is:::

    au
    authorlist
    citekey
    citenum
    ed
    editorlist

Each of these default fields are defined as "special templates". If a user defines a special template with the same name as one of the above, then the default is overwritten with the user's version. The definitions of these six default special templates are:::

    authorlist = <author.to_namelist()>
    editorlist = <editor.to_namelist()>
    citelabel = <citenum.remove_leading_zeros()>
    sortkey = <citenum>
    au = <authorlist.format_authorlist()>
    ed = <editorlist.format_editorlist()>

Note that the ordering of definitions is important. The following summarizes what these definitions are used for.

**authorlist** creates a list of dictionaries (one dictionary for each author name found within the database entry's ``author`` field). Each name dictionary has keys "first", "middle", "prefix", "last", and "suffix", where each of these keys is optional except for "last". Thus, a user can access the first and last name of the first author in the database entry using ``<authorlist.0.first> <authorlist.0.last>``. To access the middle name(s) of the second author, use ``<authorlist.1.middle>``.

**editorlist** behaves exactly as ``authorlist`` but derives its list of names from the database entry's ``editor`` field rather than ``author`` field.

**citelabel** is the thing that appears at the front of the formatted reference, and is identical to the citation label used in the manuscript to point to the item in the reference list. In technical journal articles, this is typically just a number, as in the default definition ``<citenum.remove_leading_zeros()>``. The number used here for the label indicates the order in which the entry was cited. Since the variable ``citenum`` is a string that contains leading zeros, so that the entries are properly sorted in order of 001, 002, ..., 009, 010, 011, ... and not in the strict alphabetical order of 1, 10, 11, ..., 19, 2, 20, 21, .... But for a citation label, the leading zeros are unsightly, and so we use the ``.remove_leading_zeros()`` operator to remove them from the string before creating the label.

**sortkey** is the string used to sort the entry within the reference list. For technical journal articles, what is generally wanted is just the citation order, as indicated by the ``<citenum>`` variable.

**au** is the string representing the formatted list of author names. In the default definition shown above, the name list is a standard form, and so simply uses the ``.format_authorlist()`` operator. Generally, this operator creates name lists that have the form "firstauthor" for only one author, "firstauthor and secondauthor" if only two authors, "firstauthor, secondauthor, ..., and lastauthor" if more than two authors but less than the maximum, and "firstauthor, secondauthor, ..., minauthor, et al." if more than the maximum allowed number of authors. Which author in the list is "minauthor" is defined using the ``minauthors`` option keyword. The maximum number of allowed authors is set by the ``maxauthors`` option keyword.

**ed** follows the same basic structure as ``au``, but uses the ``maxeditors`` and ``mineditors`` keywords.

Operators
---------

One can use the "dot" operator inside a variable name, as in ``<authorname.0.last.initial()>'' to perform any one of three functions: a numerical index (the ``0`` shown here), a dictionary lookup (the ``last`` used here), or the application of an operator (in this case, the ``.initial()`` operator which is used to reduce a name to its initial).

The complete list of operators available is:::

    .compress()
    .format_authorlist()
    .format_editorlist()
    .frenchinitial()
    .if_singular(var1,var2,var3)
    .initial()
    .monthabbrev()
    .monthname()
    .ordinal()
    .remove_leading_zeros()
    .sentence_case()
    .tie()
    .to_namelist()


[ADD DETAILS]



To implement BibTeX' method of reducing the capitalization state of a string (commonly used for titles), Bibulous uses a ``.sentence_case()`` operator. For example, instead of using ``<title>`` within a template, which inserts the ``title`` field from the database as-is, a user can instead insert ``<title.sentence_case()>``, which will reduce capitalization of letters in the ``title`` field (except for those letter protected within a pair of curly braces) prior to inserting them into the formatted reference.

Options keywords
----------------

A complete list of existing options keywords, together with their default definitions, is:::

    allow_scripts = False
    backrefs = False
    backrefstyle = none
    bibitemsep = None
    case_sensitive_field_names = False
    edmsg1 = , ed.
    edmsg2 = , eds
    etal_message = , \\textit{et al.}
    maxauthors = 9
    maxeditors = 5
    minauthors = 9
    mineditors = 5
    month_abbrev = True
    namelist_format = first_name_first
    period_after_initial = True
    procspie_as_journal = False
    show_urls = False
    sort_case = True
    terse_inits = False
    undefstr = ???
    use_abbrevs = True
    use_citeextract = True
    use_firstname_initials = True
    use_name_ties = False

[GIVE AN EXPLANATION OF EACH IN TURN]
