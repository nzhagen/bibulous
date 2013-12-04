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

[ADD DETAILS]

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
