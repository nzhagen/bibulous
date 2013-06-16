Python code to-do
-----------------

#. Add documentation to the Bibulous' class attributes and methods. See ``numpydoc``'s "HOWTO_DOCUMENT"
    to get this set up right.

#. BibTeX can apparently accept an optional argument to the ``\cite{}`` command and place it into
    the bibliography. Try replicating that functionality.

#. For each "Warning..." message, add a numerical tag so we know which line in the
   code they come from. (Identical messages can come from different points in
   the code, such as when the code can't find an abbreviation key.)

#. TEMPLATE LANGUAGE: Add a *name template* to the BST file, so that the template can tell the
   software how to format names without using so many options settings. Test implementing the
   "last_name_then_first" option to authorlist/editorlist formatting. Then, write a template
   function which prints the "pages" field as-is if there is a comma in the field, else it
   formats as ``<startpage>--<endpage>``. This will allow page ranges like "64--66, 87--92, 94"
   to appear in the bibliography.

   Potential example for the way to define an authorlist::

      nameformat.name = name.first.initial~name.middle.initial [name.prefix] name.last[, name.suffix]
      nameformat.<authorlist>.[nauthors==1] = nameformat.<authorlist>.0
      nameformat.<authorlist>.[nauthors==2] = nameformat.<authorlist>.0 + ' and ' + nameformat.<authorlist>.1
      nameformat.<authorlist>.[nauthors==3] = nameformat.<authorlist>.0 + ', ' + nameformat.<authorlist>.1 + ', and ' + nameformat.<authorlist>.2
      nameformat.<authorlist>.[nauthors==MAX] = (nameformat.<authorlist>.0 + ', ') ... (nameformat.<authorlist>.[MAX-1]) + ', and ' + nameformat.<authorlist>.max
      nameformat.<authorlist>.[nauthors>MAX] = (nameformat.<authorlist>.0 + ', ') ... (nameformat.<authorlist>.[MAX-1]) + ', ' + nameformat.<authorlist>.max + ', \\textit{et al.}'

#. Remember that the mandatory argument to ``\thebibliography`` in the preamble of the BBL
   file is the longest label occurring in the list. For numeric formats, this is simplify
   the largest number. For alpha-formats, it needs to be more complicated.

#. Make sure that when an exception has occurred, you still generate a valid BBL file (just
   an incomplete one). So you will need to make use of some ``try...except`` blocks.

#. Write a ``bibclean`` function which checks a ``*.bib`` file for errors. Include using
   ``namefield_to_namelist(`` to check for name format errors. A common problem will be encoding
   errors. For this, you can use ``fix_bad_unicode.py``, which attempts to undo encoding errors.
   Actually, it looks like this code has been turned into a regular Python package ``ftfy``.
   The file you have works for Python2 and not Python3, but the package is compatible with
   both.

#. Implement a bibliography format in which repeated duplicates of author names are replaced
   with a long dash. (Or ``\textit{idem}`` instead of the dash?)

#. Currently Arabic prefixes of names, like al-Turabi, will produce a space between the ``al-``
   and the last name. Need to fix.

#. On page 130 of the Biblatex documentation, it lists a ``postnote`` option to the ``\cite{}``
   command, in which the writer can enter in either a numeric page number to refer to, or a
   string that is intended to be directly appended to the line. Find a way to implement this.
   Maybe add a ``postnote`` field to the bibdata entry, and allow that field to be a list in case
   more than one citation uses different page references to the same document?

#. Note that there is an option ``use_firstname_initials``. But you don't have options for any
   other types of initials.

#. ``format_edition()``, as currently implemented, will only work for English-language
    bibliographies. This needs to be modified so that it can be made multilingual. This is actually
    even more difficult than it sounds, since many languages actually use gender-dependent
    ordinals, so that knowing the number alone is not sufficient.

#. The LaTeX packages ``natbib`` and ``biblatex`` allow the user to change the form of citation tags
    (text placed at the location of the ``\cite{}`` command in the LaTeX file). Bibulous, being only
    a backend at the moment, can't do this. Maybe work with a LaTeX package maintainer to integrate
    Bibulous into a more powerful front end?

    In addition, writing notes and annotations in the formatted bibliography is better done in the
    document itself and not the database, since these are often document-specific.

#. It may be useful for some users to extend the flexibility of the [|] notation to allow nested
    brackets.

#. For people who want to write TeX/LaTeX files in Unicode, but need to deliver an ascii file
   to a journal for their internal processing, maybe you can write a function which does the
   inverse of purify_string(). That is, it converts Unicode characters into their LaTeX
   encoded equivalents. If you work on this, the ``bibtexparser`` module has a good deal of code
   for starting on this.

Python testing to-do
--------------------

#. Add tests for each of the following::
        options.citation_order
        options.sort_case
        options.backrefs
        options.backrefstyle
        options.hyperref
        options.use_abbrevs
        options.sort_with_prefix
        options.terse_inits
        options.replace_newlines

#. Once you have the template language ready, add tests for the following:
        options.authorlist_format
        options.use_author_firstname_initials
        options.use_editor_firstname_initials
        options.editorlist_format
        options.namelist_format

#. Test that citation order options ``anyt`` and ``anyvt`` correctly implement the ``labelalpha``
    field in ``.aux`` files' ``\bibcite{}``.

#. Test ``purify_string()`` on the following::

        s1 = r"Recherches exp{\'e}rimentales sur la g{\'e}n{\'e}ralisation de l'emploi du spectrom{\`e}tre Fabry-Perot"
        s2 = r'Vorschl{\"a}ge zur Construction einiger optischer Vorichtungen'
        s3 = u'¡Hola! ¿Cómo estás? ¿Está bien así en España?'
        s4 = r'C{\'o}mo est{\'a}s? ?`Est{\'a} bien as{\'\i} en Espa{\~n}a?'
        s5 = u'Smør brød på hytte paap'
        s6 = r'Sm{\o}r br{\oo}d p{\aa} hytte p{\aap}'
        s7 = u"Rōmaji (ローマ字), kanji (漢字, かんじ), hiragana (平仮名, ひらがな), katakana (片仮名, カタカナ)"
        s8 = r'\{\{ $\left[.\left\lfloor \frac{5}{\frac{\left(3\right)}{4}} \right).\right]$ \}\}'

        print('s1 = ' + s1)
        print('s2 = ' + s2)
        print('s3 = ' + s3)
        print('s4 = ' + s4)
        print('s5 = ' + s5)
        print('s6 = ' + s6)
        print('s7 = ' + s7)
        print('s8 = ' + s8)
        print('')

        p1 = purify_string(s1)
        p2 = purify_string(s2)
        p3 = purify_string(s3)
        p4 = purify_string(s4)
        p5 = purify_string(s5)
        p6 = purify_string(s6)
        p7 = purify_string(s7)
        p8 = purify_string(s8)

        print('p1 = ' + p1)
        print('p2 = ' + p2)
        print('p3 = ' + p3)
        print('p4 = ' + p4)
        print('p5 = ' + p5)
        print('p6 = ' + p6)
        print('p7 = ' + p7)
        print('p8 = ' + p8)
        print('')

    Note that this also tests some Unicode-compatibility.

#. Test the Unicode compatibility of ``generate_sortkey()``.

#. Add a test for ``bibulous_citeextract``.

#. Test that trying to import a BibTeX-format BST file generates an ``ImportError`` exception.

#. Test proper formatting of the ``edition`` field.

#. Test for missing fields in entries.

#. The entry ``pagerange1`` has a comma-delimited page range. Currently you don't have a
    template that allows one to differentiate formatting to use the ``<pages>`` when there are
    commas in the field, whereas one uses ``<startpage>--<endpage>`` when there are no commas.
    Once you get the general parser working, give this functionality a try.

#. Add a test for locale-dependent sorting.

Template files to-do
--------------------

#. Now that you have a ``bibulous_authorextract`` script, write a
   ``cvpublications.bst`` style template file to go with it. Bibliography sections: "peer
   reviewed journal articles", "conference proceedings papers", "presentations". And
   entries should be sorted in reverse chronological order.

#. Show how to use Bibulous to create a glossary.

#. Show a style template that implements an annotated bibliography using the "annotation"
   field in the .bib database.

#. Try implementing some other BST formats, especially OSA's Opt. Lett. and SPIE's Opt. Eng.
   Note that ``chicago.sty`` uses ``chicago.bst``, and ``apalike.sty`` uses ``apalike.bst``.

#. Allow the style template parsing engine a means of setting, for example, fieldname
    ``authors`` to get mapped to fieldname ``author``. Maybe something as simple as

        entry.author = entry.authors

    or something like that.
