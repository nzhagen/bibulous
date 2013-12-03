Guidelines for writing bibliography style templates
===================================================

#. Comments begin with ``#``, following the Python convention.

#. Each template file can have as many as five sections. None of the sections are required to be in the file, but any definitions in the file must be placed inside a section header so that the code knows how to deal with the definition. The four possible section headers are: TEMPLATES, SPECIAL-TEMPLATES, OPTIONS, VARIABLES, DEFINITIONS. And note that a section header is always placed by itself on a line and has a colon appended to it, as in ``TEMPLATES:``.

#. All variable definitions use the variable name followed by whitespace, an equals sign, more whitespace, and then the definition itself. Thus the whitespace+=+whitespace is the delimiter between variable and definition, and is required syntax.

#. Inside the ``TEMPLATES`` section, all of the variable definitions are intended to map to a database entrytype name. For example::

      article = <au>, ``<title>,'' <journal>, <volume>, ...
                 [<startpage>--<endpage>|<eid>|]  (<year>). [<note>.]

   Here the ``article`` entrytype will be typeset so that the list of authors (``<au>``) is followed by the article title in double quotes, the journal name in standard font (i.e. not italics), the volume number, the page range, and the year.

#. Square brackets ``[]`` indicate an optional entry; any required entries which are not defined in the BibTeX database file (.bib file) are replaced with '???' by default. Optional arguments that are undefined are simply skipped. If a ``|`` is present within the square brackets, it indicates an "elseif" argument. If the ``|`` symbol is used to create an empty last cell, as in ``[<var>|]``, this indicates that it is required to have at least _one_ among the cells to be defined. Nesting of ``[]`` brackets is allowed, but the syntax becomes computationally expensive to parse, so that these structures should be used sparingly.

#. For users that need square brackets, ``#``, ``<``, ``>``, or ``|`` symbols as formatting elements, then simply use ``{\makeopenbracket}``, ``{\makeclosebracket}``, or ``{\makeverticalbar}``. If you need the angle brackets as formatting elements, then use ``{\makegreaterthan}`` and ``{\makelessthan}``. Note that the curly brackets are needed here so that when Bibulous replaces the command with the appropriate symbol, that symbol can be used correctly in LaTeX commands.

#. Unlike BibTeX, Bibulous does *not* change the capitalization state of any entry variables. It assumes that the authors have defined it the way they want it.

#. If an entrytype format definition contains only another entrytype on the right hand side of the ``=``, for example::

       inbook = incollection

   then this simply defines the format for the entrytype on the left hand side as identical to that of the entrytype given on the right hand side.

#. The second type of data present in the file are the formatting options. These are defined by writing ``options`` followed by a period and then the option name, for example::

      options.authorlist_format = 'first_name_first'

#. Bibulous only allows string variables to be inserted into a given position within an entrytype template, and all Bibulous variables are surrounded with angle brackets. Thus, when typesetting the bibliography, Bibulous will replace the variable ``<authorlist>`` with the string stored in the ``authorlist`` field of the current entry being formatted. An example list of variables one may choose to use is:

      ``<authorlist>``, ``<booktitle>``, ``<chapter>``, ``<edition_ordinal>``, ``<editorlist>``, ``<eid>``, ``<endpage>``, ``<institution>``, ``<journal>``, ``<nationality>``, ``<note>``, ``<number>``, ``<organization>``, ``<publisher>``, ``<school>``, ``<series>``, ``<startpage>``, ``<title>``, ``<version>``, ``<volume>``, ``<year>``.

   As one can see, these primarily consist of the various fields one can expect to see within a given BibTeX-formatted database file. This list is actually freely extensible. You can add whatever additional variables you like, so that if you use a special ``video`` field in your database, you can insert that field's value into the template wherever ``<movie>`` is located.

#. Note that several fields are defined by default which are *not* directly from the bibliography database. These are ``authorlist``, ``editorlist``, ``startpage``, ``endpage``, and ``edition_ordinal``. These fields are derived from the original database file, but have been reformatted.

#. Although the entrytype template definitions listed below are in alphabetical order, that can be put in any desired order within the file. (The exception to this rule is that if a definition consists of, for example::

      inbook = incollection

   then the ``incollection`` template must already be defined. Also note that two entrytype names are special and so cannot be used on the left hand side of the equals sign here: ``comment`` and ``preamble``.

#. A user wanting a localized form of quotation should use ``\enquote{<title>}`` rather than ````<title>''``, and add ``\usepackage{csquotes}`` to the preamble of the LaTeX document.

