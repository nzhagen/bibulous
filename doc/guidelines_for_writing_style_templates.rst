Guidelines for writing bibliography style templates
===================================================

Syntax
------

#. Comments begin with ``#``, following the Python convention.

#. Each template file can have as many as five sections. None of the sections are required to be in the file, but any definitions in the file must be placed inside a section header so that the code knows how to deal with the definition. The four possible section headers are: TEMPLATES, SPECIAL-TEMPLATES, OPTIONS, VARIABLES, DEFINITIONS. And note that a section header is always placed by itself on a line and has a colon appended to it, as in ``TEMPLATES:``.

#. The ``TEMPLATES`` section of the file contains template definitions for formatting references. The ``SPECIAL-TEMPLATES`` section contains definitions for creating variables within each database entry. The ``OPTIONS`` section contains definitions for various keywords that can be used to modify program behavior. The ``VARIABLES`` section contains user definitions for new variables to be made available. The difference between these definitions and those in ``SPECIAL-TEMPLATES`` is that the ones provided in the ``VARIABLES`` section are in-line Python code, whereas the former use templates. Finally, the ``DEFINITIONS`` section of the file contains Python-executable code that can then make functionality available in the form of template variables. (An example is provided in the *Python API* section below.

#. All variable definitions within the TEMPLATES, SPECIAL-TEMPLATES, and OPTIONS sections use the variable name followed by whitespace, an equals sign, more whitespace, and then the definition itself. Thus the [whitespace+=+whitespace] expression is the delimiter between variable and definition, and is required syntax.

#. An ellipsis ``...`` at the end of a line indicates a line continuation. All whitespace following the ellipsis, and all whitespace preceding text on the next line, is removed from the resulting connected text.

#. An ellipsis in the middle of a line indicates an "implicit loop". For details, see the *Examples for namelist formatting* section below.

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

    Another example usage would be the following:::

    author = [<著者名>|<author-en>|]

    where the ``author`` field is actually redefined to include not only the *existing* author field, but also the fields ``著者名`` or ``author-en``. That is, if the ``author`` field is missing in the database entry, the code next searches for the ``著者名`` field. If it finds it, then it will create an ``author`` field that contains a copy of the ``著者名``'s field's contents. If the ``著者名`` is also missing, the code next searches for ``author-en`` and uses that fields contents to create the missing ``author`` field.

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

One can use the "dot" operator inside a variable name, as in ``<authorname.0.last.initial()>'' to perform any one of four functions: a explicit numerical index (the ``0`` shown here), an implicit numerical index (using ``.n`` or ``.N``, for which see section *Examples for namelist formatting* below for details), a dictionary lookup (the ``last`` used here), or the application of an operator (in this case, the ``.initial()`` operator which is used to reduce a name to its initial). A numerical index must apply to a list-type of variable, and a key index must apply to a dict-type of variable (i.e. a dictionary).

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

The function of each operator is summarized below.

**.compress()** removes any whitespace found within the string. This is useful for generating namelists where the format requires "tight" spacing. An example would be "RMA Azzam", where the three initials are grouped together without spacing. And example template for generating this type of name would be::

    <authorlist.0.first><authorlist.0.middle.initial().compress()> <authorlist.0.last>

Without the ``.compress()`` operator, the name would come out as "RM A Azzam", where the two middle name initials "M" amnd "A" are spaced apart from one another by default.

**.format_authorlist()** operates on a list of dictionaries type of variable (a namelist), and uses the keyword-based default formatting scheme to create a formatted string of names. The complete list keywords that it work with is: ``etal_message``, ``maxauthors``, ``minauthors``, ``namelist_format``, ``period_after_initial``, ``terse_inits``, ``use_firstname_initials``, ``use_name_ties``. The default formatter, while fast, is not very flexible, so that users looking for more customizability will want to make use of Bibulous' implicit-index and implicit-loop based definitions. See the *Example definitions for namelist formatting* section below.

**.format_editorlist()** operates on a list of dictionaries type of variable (a namelist), and uses the keyword-based default formatting scheme to create a formatted string of names.  The complete list keywords that it work with is: ``etal_message``, ``maxeditors``, ``mineditors``, ``namelist_format``, ``period_after_initial``, ``terse_inits``, ``use_firstname_initials``, ``use_name_ties``. (The difference with the ``.format_authorlist()`` operator is that it uses ``maxeditors`` and ``mineditors`` rather than ``maxauthors`` and ``minauthors``) The default formatter, while fast, is not very flexible, so that users looking for more customizability will want to make use of Bibulous' implicit-index and implicit-loop based definitions. See the *Example definitions for namelist formatting* section below.

**.frenchinitial()** is an alternative form of the ``.initial()`` operator that has slightly different behavior. If a name begins with one of the digraphs
"Ch", "Gn", "Ll", "Ph", "Ss", or "Th", then the initial will truncate the name after the digraph instead of after the first letter.

**.if_singular(var1,var2,var3)** is an operator which inserts ``var2`` if ``var1`` has only one element, but ``var3`` if ``var1`` has more than one element. Here ``var1`` is assumed to be a list-type of variable, and ``var2`` and ``var3`` are assumed to be either fields present within the database entry or variables defined in the ``SPECIAL-TEMPLATES`` section of the file.

**.initial()** will truncate the string to its first letter. Note that if a name begins with a LaTeX markup character, such as ``{\'E}``, then the operator will convert the input string to its best attempt at a Unicode-equivalent (without character markup) prior to performing the truncation. Thus, applying the ``.initial()`` operator to the name ``{\v{Z}}ukauskas`` will produce the initialized form "Ž". 

**.monthabbrev()** assumes that the input field is a number from 1 to 12, and converts the numerical input into the abbreviated month according to the user's current locale. If the system cannot determine the user's locale, the operator will default to using the American English locale, which replaces the numerical field operated on with one of "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", or "Dec" according to the field's value. Thus, if the bibliography database entry has a field ``month = 11``, and the template has the form ``<month.monthabbrev()>``, then the template will be replaced with "Nov" for the default locale. For users with locale "Japan", this same operator will return "11月".

**.monthname()** behaves much like ``.monthabbrev()`` but rather than using an abbreviated form for the month's name, it uses the full form. Thus if the bibliography database entry has a field ``month = 3``, and the template has the form ``<month.monthname()>``, then the template variable will be replaced with "March" for the default locale. For users with locale "Norway", this same operator will return "Mars".

**.ordinal()** creates an "ordinal" from a numerical field. Thus, if the field operated on is "1", "2", "3", or "4", then the operator will replace the template with "1st", "2nd", "3rd" or "4th". Any number above 4 simply has "th" appended to the end of it. Currently Bibulous does not support non-English locales for this function. (Anyone having suggestions of how this may be implemented without too much fuss should contact us!)

**.remove_leading_zeros()** deletes any zeros from the front of the field operated on. Thus "003" will be returned as "3".

**.sentence_case()** reduces the lower case any characters in the field, except for the initial letter and any letters protected within a pair of curly braces. For example, if the database entry has ``title = {Understanding Bohmian mechanics}`` and the template has the form ``<title.sentence_case()>``, then the template variable will be replaced with "Understanding bohmian mechanics". However, if the entry has ``title = {Understanding {B}ohmian mechanics}``, the result will be "Understanding {B}ohmian mechanics".

**.tie()** replaces any spaces with an unbreakable space. Thus, "R. M. A." becomes "R.~M.~A.". An example use of this operator would be the following template:::

    authorname = [<authorlist.n.first.initial()>.~][<authorlist.n.middle.initial().tie()>. ]...
                 [<authorlist.n.prefix>~]<authorlist.n.last>[, <authorlist.n.suffix>]

**.to_namelist()** parses the field (assumed to be a BibTeX-format "and"-delimited list of names) into a Bibulous-format namelist (i.e. a list of dictionaries).

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

Each of the keywords is summarized below.

**allow_scripts** [default value: False] tells Bibulous whether to allow the evaluation of Python code in the VARIABLES and DEFINITIONS sections of ``.bst`` files. It is important for users to realize that evaluating external code in this way is a security risk, and so they should not set ``allow_scripts = True`` when inserting code that they do not trust. However, as an additional security precaution, Bibulous prevents most security-sensitive operations from being used within its Python API.

**backrefs** [default value: False] THIS KEYWORD IS NOT YET IMPLEMENTED

**backrefstyle** [default value: none] THIS KEYWORD IS NOT YET IMPLEMENTED

**bibitemsep** [default value: None] provides users a means to change the amount of vertical separation that LaTeX sets between entries in the reference list. For example, users wanting a more compact list can define ``bibitemsep = 0pt``.

**case_sensitive_field_names** [default value: False] tells Bibulous whether to consider, for example, a field named "Author" as being distinct from "author".

**edmsg1** [default value: , ed.] provides a string to use after a list of editor names, for the case when only one editor is present.

**edmsg2** [default value: , eds] provides a string to use after a list of editor names, for the case when multiple editors are present.

**etal_message** [default value: , \\textit{et al.}] provides a string to use after a truncated namelist (for example, when the number of authors exceeds the value given by the ``maxauthors`` keyword).

**maxauthors** [default value: 9] provides the maximum number of allowed names in the formatted list of authors. If the number of names is more than this, then the list of names is truncated to ``minauthors`` and the ``etal_message`` is appended to the result. (This keyword is only used within the ``.format_namelist()`` operator.)

**maxeditors** [default value: 5] provides the maximum number of allowed names in the formatted list of editors. If the number of names is more than this, then the list of names is truncated to ``mineditors`` and the ``etal_message`` is appended to the result. (This keyword is only used within the ``.format_namelist()`` operator.)

**minauthors** [default value: 9] provides the minimum number of author names to use when truncating an overlength author name list. (This keyword is only used within the ``.format_namelist()`` operator.)

**mineditors** [default value: 5] provides the minimum number of editor names to use when truncating an overlength author name list. (This keyword is only used within the ``.format_namelist()`` operator.)

**namelist_format** [default value: first_name_first, allowed values: {first_name_first, last_name_first}] defines how the formatted list of names should appear. If ``namelist_format = first_name_first`` then the individual names will appear in the order "firstname middle prefix last, suffix". If ``namelist_format = last_name_first`` then the individual names will appear in the order "prefix last, firstname middle, suffix". (This keyword is only used within the ``.format_namelist()`` operator.)

**period_after_initial** [default value: True] tells the ``.format_namelist()`` operator whether to place a period after each initial of an individual's name. Thus, if ``period_after_initial = True``, a name will appear as "R. M. A. Azzam", but if ``False`` will appear as "R M A Azzam". (This keyword is only used within the ``.format_namelist()`` operator.)

**procspie_as_journal** [default value: False] The "Proceedings of SPIE" are treated as special by the journals of the Optical Society of America. That is, they format these proceedings (and only these) in the same way that they do journal articles. Thus, a special keyword is required to allow this behavior.

**show_urls** [default value: False] informs Bibulous whether or not to use the ``hyperref`` package for placing hyperlinks into the formatted reference.

**sort_case** [default value: True] informs Bibulous whether or not to use case-sensitive sorting of reference keys.

**terse_inits** [default value: False] tells the ``.format_namelist()`` operator whether to compress together the initials of an individual's name. Thus, if ``terse_inits = True``, a name will appear as "RMA Azzam", but if ``False`` will appear as "R. M. A. Azzam". (This keyword is only used within the ``.format_namelist()`` operator.)

**undefstr** [default value: ???] informs Bibulous what kind of warning message to print when a required field is missing in the database entry.

**use_abbrevs** [default value: True] tells Bibulous whether or not to use the abbreviations defined in the bibliography database. (Used for debugging.)

**use_citeextract** [default value: True] tells Bibulous whether to perform "citation extraction", which creates a small database of only the cited items from among the complete database provided in the ``.aux`` file.

**use_firstname_initials** [default value: True] Whether or not to initialize the first names of authors in the formatted authors list. (This keyword is only used within the ``.format_namelist()`` operator.)

**use_name_ties** [default value: False] Whether or not to replace spaces with unbreakable spaces (i.e. "R. M. A. Azzam" or "R.~M.~A. Azzam") inside names in the name list. (This keyword is only used within the ``.format_namelist()`` operator.)


Examples for namelist formatting
--------------------------------

The following code provides an example usage of implicit indexing within an implicit loop structure:::

    authorlist = <author.to_namelist()>
    editorlist = <editor.to_namelist()>
    authorname.n = [<authorlist.n.first.initial()>. ][<authorlist.n.middle.initial()>. ]...
                   [<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
    au = <authorname.0>, ...,{ and }<authorname.9>
    editorname.n = [<editorlist.n.first.initial()>. ][<editorlist.n.middle.initial()>. ]...
                   [<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
    ed = <editorname.0>, ...,{ and }<editorname.2>

[EXPLAIN]


[NEED STUFF FROM TEST1 HERE, ESPECIALLY FOR SHOWING IMPLICIT INDEXING AND IMPLICIT LOOPS]

[ALSO PROVIDE AN EXAMPLE OF ``.N`` rather than just ``.n``]

Python API
----------
