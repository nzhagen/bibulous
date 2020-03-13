Guidelines for writing bibliography style templates
***************************************************

Syntax
======

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

#. Any variable placed within square brackets ``[]`` indicate that it is an optional variable --- it is not required that the database have that entry. While required entries that are not defined in the BibTeX database file (.bib file) are replaced with '???', and undefined optional variables are simply skipped. If a ``|`` is present within the square brackets, it indicates an "elseif" clause. That is, if the template is ``[<var1>|<var2> and <var3>]``, then the code will look for ``var1`` as a field within the current database entry being formatted. If it does not find the entry, then it will try the next block, where it finds the two variables ``var2`` and ``var3``. If both are defined, then the original template ``[<var1>|<var2> and <var3>]`` is replaced with ``<var2> and <var3>`` (i.e. removing the square brackets) and proceeds to replace the two variables with their corresponding fields. If either one of ``var2`` or ``var3`` is undefined in the entry, then the entire optional (bracketed) portion of the template is skipped.

#. If the ``|`` symbol is used to create an empty last cell, as in ``[<var1>|<var2>|]``, this indicates that while the individual cells within the optional block are themselves optional, it is required to have at least _one_ among the cells to be defined. Thus, ``[<note>|]`` has the same meaning as simply ``<note>`` does.

#. Nesting of ``[]`` brackets is allowed, but the syntax becomes computationally expensive to parse, so that these structures should be used sparingly.

#. Users that need to use ``[``, ``]``, ``#``, ``<``, ``>``, or ``|`` symbols as formatting elements within the reference list can implement them using some custom LaTeX-markup commands: ``{\makeopenbracket}``, ``{\makeclosebracket}``, ``{\makehashsign}``, ``{\makelessthan}``, ``{\makegreaterthan}``, ``{\makeverticalbar}``, or ``{\makeellipsis}``. Note that the curly brackets used in each case are required.

#. In the ``TEMPLATES`` section of the file, if an entrytype format definition contains only another entrytype name on the right hand side of the ``=``, i.e.::

       inbook = incollection

   then this means that the existing ``incollection`` template should be copied for use with ``inbook`` entrytypes.

#. Note that several fields are defined by default which are *not* directly from the bibliography database. These are ``au``, ``authorlist``, ``citekey``, ``citenum``, ``ed``, ``editorlist``, ``endpage``, and ``startpage``. These fields are derived from the original database file, but have been reformatted. See the *Default Fields* section below.

#. Although the entrytype template definitions listed below are in alphabetical order, that can be put in any desired order within the file. The exception to this rule is that if a definition consists of, for example::

      inbook = incollection

   then the ``incollection`` template must already be defined. Also note that two entrytype names are special and so cannot be used on the left hand side of the equals sign here: ``comment`` and ``preamble``.

#. A user wanting a localized form of quotation should use ``\enquote{<title>}`` rather than ````<title>''``, and add ``\usepackage{csquotes}`` to the preamble of the LaTeX document.

#. In the ``OPTIONS`` section of the file are the formatting options. None of these definitions are required. The complete list is given in the *Options keywords* section below, together with explanations of each.

#. The ``SPECIAL-TEMPLATES`` section is where users can define their own fields that get generated for every database entry evaluated. For example, the variable definition::

      group = [<organization>|<institution>|<corporation>|]

   in the ``SPECIAL-TEMPLATES`` section will create a ``group`` field that can be used as the variable ``<group>`` within the regular ``TEMPLATES`` section of the file. This effectively allows users to create a shortcut. Where they could write out ``[<organization>|<institution>|<corporation>|]`` inside each template that needs this structure, the special template definition allows them to replace each instance with a simple ``<group>``.

   Another example usage would be the following::

      author = [<author-en>|<author-jp>|]

   where the ``author`` field is actually redefined to include not only the *existing* author field, but also the fields ``author-en`` or ``author-jp``. That is, if the ``author`` field is missing in the database entry (the field matching the thing on the left hand side), the code next searches for the ``author-en`` field. If it finds it, then it will create an ``author`` field that contains a copy of the ``author-en``'s field's contents. If the ``author-en`` is also missing, the code next searches for ``author-jp`` and uses that fields contents to create the missing ``author`` field. This is a convenient way of grouping different variable names in order to simplify templates.

#. The order in which any definitions are placed within the special templates is important. For example, if a user has ``au = <authorlist.format_authorlist()>`` and then below that defines ``authorlist = <author.to_namelist()>``, then the code will issue an error stating that ``authorlist`` is not defined when attempting to create the ``au`` variable. Since the definition for ``au`` assumes the presence of the ``authorlist`` variable, the latter definition must be placed above it.

Default Fields
==============

A complete list of the existing default fields is:::

    au
    authorlist
    citealnum
    citealpha
    citekey
    citenum
    ed
    editorlist
    sortkey
    sortnum

Each of these default fields are defined as "special templates". If a user defines a special template with the same name as one of the above, then the default is overwritten with the user's version. The definitions of the default special templates are:::

    authorlist = <author.to_namelist()>
    editorlist = <editor.to_namelist()>
    citealnum = ?
    citelabel = <citenum>
    sortkey = <citenum>
    au = <authorlist.format_authorlist()>
    ed = <editorlist.format_editorlist()>

Note that the ordering of definitions is important (that is, if ``citelabel`` uses ``authorlist`` in its definition, then the latter has to appear before it in the list of special templates, so that it is defined by the time that ``citelabel`` needs to be defined). The following summarizes what these definitions are used for.

Also, in addition to these default fields, there are also four special variables defined, ``citealpha``, ``citealnum``, ``citenum``, and ``sortnum``. These can be accessed as ``<citealpha>``, ``<citealnum>``, ``<citenum>``, and ``<sortnum>`` within any template. The first, ``<citealpha>``, is designed to reproduce the citation label style used by BibTeX's ``alpha`` style. For example, ``GKP94`` is the ``alpha``--style citation label for the book *Concrete Mathematics*, 2nd Edition, by Ronald L. Graham, Donald E. Knuth, and Oren Patashnik (1994). The second variable ``<citealnum>`` is a variant of this that creates a citation label from the first letter of the author's last name, followed by an integer indicating its place in the sorted bibliography. Thus the book by Graham *et al.* would have the label "G2" if preceded by, say, *Introduction to Fourier Optics* by Joseph W. Goodman (1968), since the latter, being published earlier, would be placed earlier in the sorted list. ``<citenum>`` is simply the numerical order in which the reference was cited in the text (starting at 1 with the first citation). ``<sortnum>`` is the numerical order in which the citation appears in the reference list. If the reference list is sorted alphabetically, for example, then ``sortnum`` will generally be different from ``citenum``.

**au** is the string representing the formatted list of author names. In the default definition shown above, the name list is a standard form, and so simply uses the ``.format_authorlist()`` operator. Generally, this operator creates name lists that have the form "firstauthor" for only one author, "firstauthor and secondauthor" if only two authors, "firstauthor, secondauthor, ..., and lastauthor" if more than two authors but less than the maximum, and "firstauthor, secondauthor, ..., minauthor, et al." if more than the maximum allowed number of authors. Which author in the list is "minauthor" is defined using the ``minauthors`` option keyword. The maximum number of allowed authors is set by the ``maxauthors`` option keyword.

**authorlist** creates a list of dictionaries (one dictionary for each author name found within the database entry's ``author`` field). Each name dictionary has keys "first", "middle", "prefix", "last", and "suffix", where each of these keys is optional except for "last". Thus, a user can access the first and last name of the first author in the database entry using ``<authorlist.0.first> <authorlist.0.last>``. To access the middle name(s) of the second author, use ``<authorlist.1.middle>``.

**citealnum** is a field generated by taking the first letter of the first author's last name, and appending to it the citation sort order number within all entries sharing that prefix. Thus "Bugs Bunny" would have a ``citealnum`` of "B" followed by its order number. If "Yogi Bear" were another first-author name in the list, then "Yogi Bear" would receive ``citealnum = B1`` while "Bugs Bunny" would receive ``citealnum = B2``.

**citealpha** is a field generated according to BibTeX's classic "alpha" style. That is, it takes the first three letters of the author's last name if there is only one author. If multiple authors, it takes the initials of the author last names, for up to the first three authors. If no author is present, then it looks for the first three letters of the ``organization`` field. Finally, the three-letter alphabetical label is followed by the last two digits of the publication year. Thus, any user wishing to use BibTeX's classic ``alpha`` style for citation labels can use ``citelabel = <citealpha>`` in the SPECIAL-TEMPLATES section of the file.

**citelabel** is the thing that appears at the front of the formatted reference, and is identical to the citation label used in the manuscript to point to the item in the reference list. In technical journal articles, this is typically just a number, as in the default definition ``<citenum>``. The number used here for the label indicates the order in which the entry was cited.

**ed** follows the same basic structure as ``au``, but uses the ``maxeditors`` and ``mineditors`` keywords.

**editorlist** behaves exactly as ``authorlist`` but derives its list of names from the database entry's ``editor`` field rather than ``author`` field.

**sortkey** is the string used to sort the entry within the reference list. For technical journal articles, what is generally wanted is just the citation order, as indicated by the ``<citenum>`` variable.

Operators
---------

One can use the "dot" operator inside a variable name, as in ``<authorname.0.last.initial()>'' to perform any one of five functions: a explicit numerical index (the ``0`` shown here, listed as the ``.#`` operator below), an implicit numerical index (using ``.n`` or ``.N``, for which see section *Examples for namelist formatting* below for details), a range index (listed as the ``##:##`` operator below), a dictionary lookup (the ``last`` used here), or the application of an operator (in this case, the ``.initial()`` operator which is used to reduce a name to its initial). A numerical index must apply to a list-type of variable, and a key index must apply to a dict-type of variable (i.e. a dictionary). Note that, due to limitations of the parser, it is not allowed for ``<.>`` angle-bracketed variables to be placed within other angle-bracketed variables. Thus, function arguments take variable names with their angle brackets removed.

The complete list of operators available is:::

    .#
    .##:##
    .compress()
    .exists()
    .format_authorlist()
    .format_editorlist()
    .frenchinitial()
    .if_len_equals(var1,number,var2,var3)
    ..    .if_len_less_than(var1,number,var2,var3)
    ..    .if_len_more_than(var1,number,var2,var3)
    .if_str_equal(test_str,then_var,else_var)
    .if_singular(var1,var2,var3)
    .initial()
    .len()
    .lower()
    .monthabbrev()
    .monthname()
    .n
    .N
    .null()
    .ordinal()
    .purify()
    .replace(old,new)
    .sentence_case()
    .tie()
    .to_namelist()
    .uniquify(arg)
    .upper()
    .zfill(num)

The function of each operator is summarized below.

**.#** An explicit numerical index, i.e., select the #th element of the operand.

**.##:##** A range index, i.e., select the ##th through ##th elements of the operand. For example, for a bibliography entry whose database file contains ``title = {Impossibility}``, a template variable of the form ``<title.0:2>`` will return ``Imp``, and ``<title.3:5>`` will return ``oss``. The first character of the operand thus has an index ``0``. Indexing from the end of the operand can be done using negative number indices. For example, the last character of the operand can be indexed by ``-1``, and the third to last by ``-3``, so that in the example above, ``<title.-3:-1>`` will return ``ity``.

**.compress()** removes any whitespace found within the string. This is useful for generating namelists where the format requires "tight" spacing. An example would be "RMA Azzam", where the three initials are grouped together without spacing. And example template for generating this type of name would be::

    <authorlist.0.first><authorlist.0.middle.initial().compress()> <authorlist.0.last>

Without the ``.compress()`` operator, the name would come out as "RM A Azzam", since the two middle name initials "M" and "A" are spaced apart from one another by default.

**.exists()** returns empty braces ``{}`` if the variable is defined (i.e. "do nothing --- just check for existence"), else evaluate as "undefined".

**.format_authorlist()** operates on a list of dictionaries type of variable (a namelist), and uses the keyword-based default formatting scheme to create a formatted string of names. The complete list keywords that it looks for is: ``etal_message``, ``maxauthors``, ``minauthors``, ``namelist_format``, ``period_after_initial``, ``terse_inits``, ``use_firstname_initials``, ``use_name_ties``. The default formatter, while fast, is not very flexible, so that users looking for more customizability will want to make use of Bibulous' implicit-index and implicit-loop based definitions. See the *Example definitions for namelist formatting* section below.

**.format_editorlist()** operates on a list of dictionaries type of variable (a namelist), and uses the keyword-based default formatting scheme to create a formatted string of names.  The complete list keywords that looks for is: ``etal_message``, ``maxeditors``, ``mineditors``, ``namelist_format``, ``period_after_initial``, ``terse_inits``, ``use_firstname_initials``, ``use_name_ties``. (The difference with the ``.format_authorlist()`` operator is that it uses ``maxeditors`` and ``mineditors`` rather than ``maxauthors`` and ``minauthors``) The default formatter, while fast, is not very flexible, so that users looking for more customizability will want to make use of Bibulous' implicit-index and implicit-loop based definitions. See the *Example definitions for namelist formatting* section below.

**.frenchinitial()** is an alternative form of the ``.initial()`` operator that has slightly different behavior. If a name begins with one of the digraphs "Ch", "Gn", "Ll", "Ph", "Ss", or "Th", then the initial will truncate the name after the digraph instead of after the first letter.

**.if_str_equal(test_str,then_var,else_var)** inserts ``then_var`` if the string to be operated on is equal to ``test_str``, else it inserts the string ``else_var``.

**.if_singular(var,res1,res2)** inserts ``res1`` if ``var`` has only one element, but ``res2`` if ``var`` has more than one element. Here ``var`` is assumed to be a list-type of variable. An example usage is the following: ``[<ed.if_singular(editorlist, option.edmsg1), option.edmsg2)>, ]``. This form appends the contents of the ``edmsg1`` option variable to the end of the ``ed`` variable if the ``editorlist`` variable contains only one element (is singular). If ``editorlist`` has more than one element, then the contents of the ``edmsg2`` variable is appended instead. (This could potentially be a null string.)

**.if_num_equals(var,number,res1,res2)** appends ``res1`` if ``var`` equals ``number``, but otherwise appends ``var2``.

.. **.if_less_than(var,number,res1,res2)** appends ``res1`` if ``var`` is less than ``number``, but otherwise appends ``res2``.

.. **.if_more_than(var,number,res1,res2)** appends ``res1`` if ``var`` is more than ``number``, but otherwise appends ``res2``.

**.initial()** will truncate the string to its first letter. Note that if a name begins with a LaTeX markup character, such as ``{\'E}``, then the operator will convert the input string to its best attempt at a Unicode-equivalent (without character markup) prior to performing the truncation. Thus, applying the ``.initial()`` operator to the name ``{\v{Z}}ukauskas`` will produce the initialized form "Ž".

**.len()** returns the number of elements in a list variable (to the left of the operator dot).

**.lower()** reduces all letters in its argument to lower case. If any LaTeX markup letters exist in the argument, then they will be converted to Unicode equivalents first before applying the operator. Thus, if the field ``au`` contains ``{\AA}`` then the operator will first convert this to the letter Å and then reduce it to the lower case å.

**.monthabbrev()** assumes that the input field is a number from 1 to 12, and converts the numerical input into the abbreviated month according to the user's current locale. If the system cannot determine the user's locale, the operator will default to using the American English locale, which replaces the numerical field operated on with one of "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", or "Dec" according to the field's value. Thus, if the bibliography database entry has a field ``month = 11``, and the template has the form ``<month.monthabbrev()>``, then the template will be replaced with "Nov" for the default locale. For users with locale "Japan", this same operator will return "11月".

**.monthname()** behaves much like ``.monthabbrev()`` but rather than using an abbreviated form for the month's name, it uses the full form. Thus if the bibliography database entry has a field ``month = 3``, and the template has the form ``<month.monthname()>``, then the template variable will be replaced with "March" for the default locale. For users with locale "Norway", this same operator will return "Mars".

**.n** See the *Examples for namelist formatting* below

**.N** [Not currently supported]

**.null()** returns an undefined variable, forcing the string to be evaluated as "undefined".

**.ordinal()** creates an "ordinal" from a numerical field. Thus, if the field operated on is "1", "2", "3", or "4", then the operator will replace the template with "1st", "2nd", "3rd" or "4th". Any number above 4 simply has "th" appended to the end of it. Currently Bibulous does not support non-English locales for this function. (Anyone having suggestions of how this may be implemented without too much fuss should contact us!)

**.purify()** attempts to convert its argument into a string without LaTeX-markup for foreign characters. Thus, if the entry contains ``title = {{\AA}land}`` then a template variable of the form ``<title.purify()>`` will produce the result ``Åland``. This can be useful when having to use ``substr_replace()`` and other functions where the markup may cause matching problems.

**.replace(old,new)** will replace the substring ``old`` with ``new`` wherever it finds ``old`` within the string it is applied to. For example, if a user wants to make the name "J. W. Tukey" bold everywhere it appears in a reference, then ``.replace(J. W. Tukey,\textbf{J. W. Tukey})`` will work. Note that whitespace is preserved here. Thus, ``.replace(J. W. Tukey, \textbf{J. W. Tukey})`` will add a space in front of ``\textbf{J. W. Tukey}``. Also, Bibulous will not allow the use of ``<``, ``>``, ``|``, or ``)`` characters in the two arguments of the operator.

**.sentence_case()** reduces the lower case any characters in the field, except for the initial letter and any letters protected within a pair of curly braces. For example, if the database entry has ``title = {Understanding Bohmian mechanics}`` and the template has the form ``<title.sentence_case()>``, then the template variable will be replaced with "Understanding bohmian mechanics". However, if the entry has ``title = {Understanding {B}ohmian mechanics}``, the result will be "Understanding {B}ohmian mechanics".

**.tie()** replaces any spaces with an unbreakable space. Thus, "R. M. A." becomes "R.~M.~A.". An example use of this operator would be the following template:::

    authorname = [<authorlist.n.first.initial()>.~][<authorlist.n.middle.initial().tie()>. ]...
                 [<authorlist.n.prefix>~]<authorlist.n.last>[, <authorlist.n.suffix>]

**.to_namelist()** parses the field (assumed to be a BibTeX-format "and"-delimited list of names) into a Bibulous-format namelist (i.e. a list of dictionaries).

**.uniquify(arg)** appends a letter character (if arg=``a``) or a number (if arg=``1``) to the end of the field to make it unique relative to the same field in every other cited entry. For example, if two authors have the name "Smith" and published a paper in the year 2000, then the template ``citelabel = <authorlist.0.last><year>`` will produce the same citation label for both entries. Thus, we can rename this as ``citetemp = <authorlist.0.last><year>`` and then define ``citelabel = <citetemp.uniquify(a)>`` to generate unique labels. For this example, the first citation will have the label "Smith2000" and the second "Smith2000a". If a third citation shares the same name and year, then it will be given the unique label "Smith2000b", and so on.

**.upper()** raises all letters in its argument to upper case. If any LaTeX markup letters exist in the argument, then they will be converted to Unicode equivalents first before applying the operator. Thus, if the field ``au`` contains ``{\aa}`` then the operator will first convert this to the letter å and then raise it to the upper case Å.

**.zfill(num)** appends zeros to the front of its argument, where ``num`` indicates the desired final length of the string. For example, if the field ``vol`` contains the number ``11``, then calling ``<vol.zfill(3)>`` produces the result ``011``.

Options keywords
================

A complete list of existing options keywords, together with their default definitions, is:::

    allow_scripts = False
    autocomplete_doi = True
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
    name_separator = and
    namelist_format = first_name_first
    period_after_initial = True
    procspie_as_journal = False
    sort_case = True
    sort_order = forward
    terse_inits = False
    undefstr = ???
    use_abbrevs = True
    use_citeextract = True
    use_firstname_initials = True
    use_name_ties = False

Each of the keywords is summarized below.

**allow_scripts** [default value: False] tells Bibulous whether to allow the evaluation of Python code in the VARIABLES and DEFINITIONS sections of ``.bst`` files. It is important for users to realize that evaluating external code in this way is a security risk, and so they should not set ``allow_scripts = True`` when inserting code that they do not trust. However, as an additional security precaution, Bibulous prevents most security-sensitive operations from being used within its Python API.

**autocomplete_doi** [default value: True] tells Bibulous whether to add ``http://dx.doi.org/`` to the front of the ``doi`` field if the front is missing. This allows the ``<doi>`` variable to be used as a complete URL, even when the prefix is missing in the database field.

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

**name_separator** [default value: and] informs Bibulous how to separate the individual names in a BibTeX-format field of names. For example, with a BibTeX-format field of ``Bugs Bunny and Porky Pig``, using the separator ``and`` allows Bibulous to determine that there are two separate people, ``Bugs Bunny`` and ``Porky Pig``. If the option keyword has an empty field (*i.e.* it is written as ``name_separator =``, with nothing on the right hand side of the equals) then it is assumed that the intended separator is a space character. This is useful for alphabets (such as Chinese and Japanese) that often work without spaces.

**namelist_format** [default value: first_name_first, allowed values: {first_name_first, last_name_first}] defines how the formatted list of names should appear. If ``namelist_format = first_name_first`` then the individual names will appear in the order "firstname middle prefix last, suffix". If ``namelist_format = last_name_first`` then the individual names will appear in the order "prefix last, firstname middle, suffix". (This keyword is only used within the ``.format_namelist()`` operator.)

**period_after_initial** [default value: True] tells the ``.format_namelist()`` operator whether to place a period after each initial of an individual's name. Thus, if ``period_after_initial = True``, a name will appear as "R. M. A. Azzam", but if ``False`` will appear as "R M A Azzam". (This keyword is only used within the ``.format_namelist()`` operator.)

**procspie_as_journal** [default value: False] The "Proceedings of SPIE" are treated as special by the journals of the Optical Society of America. That is, they format these proceedings (and only these) in the same way that they do journal articles. Thus, a special keyword is required to allow this behavior.

**sort_case** [default value: True] informs Bibulous whether or not to use case-sensitive sorting of reference keys.

**sort_order** [default value: forward] whether to sort in increasing order (``forward``) or decreasing order (``reverse``).

**terse_inits** [default value: False] tells the ``.format_namelist()`` operator whether to compress together the initials of an individual's name. Thus, if ``terse_inits = True``, a name will appear as "RMA Azzam", but if ``False`` will appear as "R. M. A. Azzam". (This keyword is only used within the ``.format_namelist()`` operator.)

**undefstr** [default value: ???] informs Bibulous what kind of warning message to print when a required field is missing in the database entry.

**use_abbrevs** [default value: True] tells Bibulous whether or not to use the abbreviations defined in the bibliography database. (Used for debugging.)

**use_citeextract** [default value: True] tells Bibulous whether to perform "citation extraction", which creates a small database of only the cited items from among the complete database provided in the ``.aux`` file.

**use_firstname_initials** [default value: True] Whether or not to initialize the first names of authors in the formatted authors list. (This keyword is only used within the ``.format_namelist()`` operator.)

**use_name_ties** [default value: False] Whether or not to replace spaces with unbreakable spaces (i.e. "R. M. A. Azzam" or "R.~M.~A. Azzam") inside names in the name list. (This keyword is only used within the ``.format_namelist()`` operator.)


Implicit loops and examples for namelist formatting
===================================================

The following code provides an example usage of implicit indexing within an implicit loop structure:::

    authorlist = <author.to_namelist()>
    editorlist = <editor.to_namelist()>
    authorname.n = [<authorlist.n.first.initial()>. ][<authorlist.n.middle.initial()>. ]...
                   [<authorlist.n.prefix> ]<authorlist.n.last>[, <authorlist.n.suffix>]
    au = <authorname.0>, ...,{ and }<authorname.9>
    editorname.n = [<editorlist.n.first.initial()>. ][<editorlist.n.middle.initial()>. ]...
                   [<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]
    ed = <editorname.0>, ...,{ and }<editorname.2>

Here the ``authorlist`` and ``editorlist`` definitions create namelist variables from the ``author`` and ``editor`` fields in the entry (if they exist). Next, the implicitly-indexed ``authorname.n`` cannot operate except within an implicit loop, and so we should describe that first. It is easier to describe the functionality of the ``ed`` template than the ``au`` one, as it has a smaller number of allowed names. The ``ed`` template has the definition::

    <editorname.0>, ...,{ and }<editorname.2>

which simplifies to ``<editorname.0>`` when there is only one editor in the database entry, and::

    <editorname.0> and <editorname.1>

when there are only two. Here the separator `` and `` comes from the ``{ and }`` placed at the right hand side of the implicit loop. For three editors, the implicit loop expands the template to::

    <editorname.0>, <editorname.1>, and <editorname.2>

where this time the comma alone is used as the first delimiter, as it is outside the enclosed braces. For the final element, both the comma and the ``{ and }`` at the right hand side of the implicit loop are used as the final delimiter. Since the template does not specify the format for more than three editor names, the code builds an *et al.* construction when there more than this number of names, so that the result becomes::

    <editorname.0>, <editorname.1>, <editorname.2>, \textit{et al.}

where the form of the string ``\textit{, et. al}`` is specified by the ``etal_message`` keyword option.

Thus, the implicit loop has filled out a unique template based on the number of editors it finds within the database entry. The next step is to use the implicitly-indexed ``editorname`` to complete building out the template. The latter template is defined as::

    editorname.n = [<editorlist.n.first.initial()>. ][<editorlist.n.middle.initial()>. ]...
                   [<editorlist.n.prefix> ]<editorlist.n.last>[, <editorlist.n.suffix>]

so that a template variable of the form ``<editorname.0>'' is replaced with::

    [<editorlist.0.first.initial()>. ][<editorlist.0.middle.initial()>. ]...
    [<editorlist.0.prefix> ]<editorlist.0.last>[, <editorlist.0.suffix>]

That is, the implicit index ``.n`` is everywhere replaced with the explicit index ``0``. For the case of a database entry containing two editor names, the final template will thus have the form::

    [<editorlist.0.first.initial()>. ][<editorlist.0.middle.initial()>. ]...
    [<editorlist.0.prefix> ]<editorlist.0.last>[, <editorlist.0.suffix>] and ...
    [<editorlist.1.first.initial()>. ][<editorlist.1.middle.initial()>. ]...
    [<editorlist.1.prefix> ]<editorlist.1.last>[, <editorlist.1.suffix>]

With this template now complete, the code begins to evaluate the entry and replace the individual variables with their corresponding database fields.

Python API
==========

Bibulous also provides to users an extensible Python interface allowing users to directly manipulate Bibulous' internal data structures. These use the ``VARIABLES`` and ``DEFINITIONS`` sections of the file, as shown below. For the ```VARIABLES`` section, a variable name is defined (the first example below defines the variable ``year_bce``, while the second example below defines ``pagerange``). On the right hand side of the definition, however, is a Python function call. This is different from the other sections of the BST file, which use template syntax. Any variable defined in this way within the ``VARIABLES`` section can then be accessed as a template variable (i.e. ``<year_bce>``) within the ``TEMPLATES`` section of the file. Two example uses are shown below.

To allow Bibulous to read the ``VARIABLES`` and ``DEFINITIONS`` sections of the file, users must set the option keyword ``allow_scripts`` to True.

**First example: a custom yearstyle**. For a bibliography containing works from authors dating from before year 0, a common approach is to append "BC" to the year number, and for positive-numbered years, appending "AD". More recently, the convention has been to append "BCE" and "CE" rather than "BC" and "AD". The example defines an option keyword ``yearstyle`` that allows users to switch between one style (BC/AD) and the other (BCE/CE). This keyword is accessed by placing ``options`` as an argument to the ``format_yearstyle()`` function defining the variable ``year_bce``. Inside the function, it can then check the options dictionary for the ``yearstyle`` keyword and determine which convention to use.

The ``format_yearstyle()`` function itself is straightforward. It first checks whether the entry has a ``year`` field. If not, then it returns ``None``, indicating that the function's result is undefined. If it finds a ``year`` field, then it checks to see whether it corresponds to an integer. If not, then it returns the field as-is. (Perhaps a user defines his ``year`` fields as ``45 BCE`` with the BCE already written out inside the field?) If it finds an integer value, then it determines which style to use (BC/AD or BCE/CE). If the year number is negative then it appends "BC" or "BCE to the end. If the year number is positive then it appends "AD" or "CE to the end, depending on the convention chosen.

Example::

    OPTIONS:
    allow_scripts = True
    yearstyle = BCE/CE

    VARIABLES:
    year_bce = format_yearstyle(entry, options)

    DEFINITIONS:
    ## NOTE! Only Unix-style line endings are allowed here.
    def format_yearstyle(entry, options):
        '''
        Append "BC or "AD" to "year", depending on whether the year is positive or negative.
        If the option "yearstyle" is set to "BCE/CE", then use "BCE" and "CE" instead of "BC"
        and "AD".
        '''

        if ('year' not in entry):
            return(options['undefstr'])

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

**Second example: a custom pagestyle**. For a bibliography containing works from magazines, it is not uncommon to find articles with large gaps in page numbers. Here is an example bibliography database entry::

    @article{stewart,
    title = {Interview with Walter Stewart},
    author = {Doug Stewart},
    journal = {Omni},
    year = {1989},
    volume = {11},
    number = {5},
    pages = {64--66, 87--92, 94}
    }

where we can see that the article was broken into three sections in order to fit the editors' formatting requirements. Many bibliography styles require a starting and ending page, but these are misleading when the article is broken across pages in this way. Thus, a user may want to have the option that if a comma is found within the ``pages`` field of an entry then it should be displayed as-is. If no comma is found, then it simply returns the standard startpage--endpage pair.

To make this work, first the option ``allow_scripts`` must be set to true. Next, a new ``pagerange`` variable is defined, so that it can be accessed in the ``TEMPLATES`` section of the file as ``<pagerange>``. The variable is defined as the return value of the function ``format_pagerange()`` given in the ``DEFINITIONS`` section. The defined function first checks to see if there is a ``pages`` field defined in the entry. If not, then it returns None, so that the ``pagerange`` variable will also be undefined. If it finds the ``pages`` field, it looks to see if there is a comma present. If so, it returns the field as-is. If not, it looks for the ``endpage`` variable (generated by default by Bibulous from the ``pages`` field). If present, then the function returns a startpage--endpage pair. If ``endpage`` is not present, then it returns only the ``startpage`` variable.

Example::

    OPTIONS:
    allow_scripts = True

    VARIABLES:
    pagerange = format_pagerange(entry, options)

    DEFINITIONS:
    def format_pagerange(entry, options):
        '''
        If the "pages" field is comma-delimited, then return the pages field as-is. Otherwise
        return the standard startpage--endpage range.
        '''

        if not ('pages' in entry):
            return(None)
        elif (',' in entry['pages']):
            return(entry['pages'])
        elif ('endpage' in entry):
            return(entry['startpage']--entry['endpage'])
        else:
            return(entry['startpage'])
