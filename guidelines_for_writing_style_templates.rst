Guidelines for writing bibliography style templates
===================================================

#. Comments begin with ``#``. (A single ``#`` indicates a symbol and not a comment!)

#. A line which begins with an entrytype name followed by an ``=`` sign defines the bibliographic
format for that entrytype. For example::

      article = <authorlist>, ``<title>,'' <journal>, <volume>, [<startpage>--<endpage>|<eid>|]  (<year>). [<note>.]

   Here the ``article`` entrytype will be typeset so that the list of authors is followed by the
   article title in double quotes, the journal name in standard font (i.e. not italics), the volume
   number, the page range, and the year.

#. Square brackets ``[]`` indicate an optional entry; any required entries which are not defined
   in the BibTeX database file (.bib file) are replaced with '???' by default. Optional arguments is
   undefined are simply skipped. If a ``|`` is present within the square brackets, it indicates an
   "elseif" argument (if not the final ``|`` within the brackets), or an "else" argument (if the
   final ``|``). The "else" indicates a *required* argument, so if you want an optional entry to be
   replaced with something, you can use ``[option|]`` --- the use of an empty cell inside the square
   brackets indicates that we simply use the default replacement for an undefined required argument
   (i.e. ``???``). If you want all of the cells to be optional, then use ``|'']`` in the last cell
   -- that is, the last cell should be an empty string. For  now, the format currently does not
   allow nesting of brackets.

#. If you need the square brackets or ``|`` symbol as formatting elements, then simply use
   ``{\makeopenbracket}``, ``{\makeclosebracket}``, or ``{\makeverticalbar}``. If you need the angle
   brackets as formatting elements, then use ``{\makegreaterthan}`` and ``{\makelessthan}``. Note
   that the curly brackets are needed here so that when Bibulous replaces the command with the
   appropriate symbol, that symbol can be used correctly in LaTeX commands.

#. Unlike BibTeX, Bibulous does *not* change the capitalization state of any entry variables. It
   assumes that the authors have defined it the way they want it.

#. If an entrytype format definition contains only another entrytype on the right hand side of the
   ``=``, for example::

       inbook = incollection

   then this simply defines the format for the entrytype on the left hand side as identical to that
   of the entrytype given on the right hand side.

#. The second type of data present in the file are the formatting options. These are defined by
   writing ``options`` followed by a period and then the option name, for example::

      options.authorlist_format = 'first_name_first'

#. Bibulous only allows string variables to be inserted into a given position within an entrytype
   template, and all Bibulous variables are surrounded with angle brackets. Thus, when typesetting
   the bibliography, Bibulous will replace the variable ``<authorlist>`` with the string stored
   in the ``authorlist`` field of the current entry being formatted. An example list of variables
   one may choose to use is:

      ``<authorlist>``, ``<booktitle>``, ``<chapter>``, ``<edition_ordinal>``, ``<editorlist>``,
      ``<eid>``, ``<endpage>``, ``<institution>``, ``<journal>``, ``<nationality>``, ``<note>``,
      ``<number>``, ``<organization>``, ``<publisher>``, ``<school>``, ``<series>``,
      ``<startpage>``, ``<title>``, ``<version>``, ``<volume>``, ``<year>``.

   As one can see, these primarily consist of the various fields one can expect to see within a
   given BibTeX-formatted database file. This list is actually freely extensible. You can add
   whatever additional variables you like, so that if you use a special ``video`` field in your
   database, you can insert that field's value into the template wherever ``<movie>`` is located.

#. Note that several fields are defined by default which are *not* directly from the bibliography
   database. These are ``authorlist``, ``editorlist``, ``startpage``, ``endpage``, and
   ``edition_ordinal``. These fields are derived from the original database file, but have been
   reformatted.

#. Although the entrytype template definitions listed below are in alphabetical order, that can be
   put in any desired order within the file. (The exception to this rule is that if a definition
   consists of, for example::

      inbook = incollection

   then the ``incollection`` template must already be defined. Also note that two entrytype names
   are special and so cannot be used on the left hand side of the equals sign here: ``comment`` and
   ``preamble``.

#. Options for ``citation_order`` include

      * ``citenumber`` or ``none`` (the default)
      * ``citekey``
      * ``alpha`` (uses three letters of author's last name plus last two numbers in the year)
      * ``nyt`` or ``plain`` (uses the first author's last name, the year, and then the title)
      * ``nty``, ``nyvt``, ``anyt``, ``anyvt``, ``ynt``, and ``ydnt``

   where the different letters indicate (as in Biblatex) ``n`` = name (i.e. author's last name),
   ``y`` = year, ``t`` = title, ``v`` = volume, and ``a`` = alphabetic label (where the user is
   implementing some bibliography front-end that prints out alphabetic labels inside the ``.aux``
   file). The ``d`` here means that the order should be *descending* rather than the default of
   ascending.

#. A user wanting a localized form of quotation can replace, for example, ````<title>''`` with
   ``\enquote{<title>}`` and setting the option ``use_csquotes`` to True. In the LaTeX document,
   this requires that the user make sure that the csquotes package is imported (using
   ``\usepackage{csquotes}``) in the preamble.
