Python code to-do
-----------------

#. Put some simple safeties into the API engine. Such as: prevent imports and file operations. Prevent
   use of os and sys modules. And some of the built-in functions as well. And add an option that the
   user can set --- "allow_scripts" --- which defaults to "False".

#. Add an optional argument to Bibulous' command-line interface, giving user preferences about running
   scipts. That is, the user can opt to either run scripts as-is when it finds them in the BST files,
   or it can skip any scripts, in the interest of safety. The latter should be the default.

   Additionally, we need to make sure that there are no uses of os.* or sys.* within the user's script.
   We need to remove all "import" statements. Also we must remove all uses of the open() and write()
   functions to prevent use of external files.

#. Add documentation to the Bibulous' class attributes and methods. See ``numpydoc``'s "HOWTO_DOCUMENT"
   to get this set up right.

#. Simplify the ``parse_bibfield()`` method by taking some of the function's load off into a subroutine.

#. The ``format_bibitem()`` method is another overly complex function that needs simplifying.

#. BibTeX can apparently accept an optional argument to the ``\cite{}`` command and place it into
   the bibliography. Try replicating that functionality.

#. For each "Warning..." message, add a numerical tag so we know which line in the
   code they come from. (Identical messages can come from different points in
   the code, such as when the code can't find an abbreviation key.)

#. Remember that the mandatory argument to ``\thebibliography`` in the preamble of the BBL
   file is the longest label occurring in the list. For numeric formats, this is simplify
   the largest number. For alpha-formats, it needs to be more complicated.

#. Make sure that when an exception has occurred, you still generate a valid BBL file (just
   an incomplete one). So you will need to make use of some ``try...except`` blocks.

#. Add the "Example" section to the Bibdata class docstring.

#. Write a ``bibclean`` function which checks a ``*.bib`` file for errors. Include using
   ``namefield_to_namelist()`` to check for name format errors. A common problem will be encoding
   errors. For this, you can use ``fix_bad_unicode.py``, which attempts to undo encoding errors.
   Actually, it looks like this code has been turned into a regular Python package ``ftfy``.
   The file you have works for Python2 and not Python3, but the package is compatible with
   both.

#. Implement a bibliography format in which repeated duplicates of author names are replaced
   with a long dash. (Or ``\textit{idem}`` instead of the dash?)

#. Currently Arabic prefixes of names, like al-Turabi, will produce a space between the ``al-``
   and the last name. Need to fix. Or maybe just let users make their own template script to
   handle that case?

#. ``format_edition()``, as currently implemented, will only work for English-language
    bibliographies. This needs to be modified so that it can be made multilingual. This is actually
    even more difficult than it sounds, since many languages actually use gender-dependent
    ordinals, so that knowing the number alone is not sufficient.

#. The LaTeX packages ``natbib`` and ``biblatex`` allow the user to change the form of citation tags
   (text placed at the location of the ``\cite{}`` command in the LaTeX file). Bibulous, being only
   a backend at the moment, can't do this. Maybe work with a LaTeX package maintainer to integrate
   Bibulous into a more powerful front end? In addition, writing notes and annotations in the formatted
   bibliography is better done in the document itself and not the database, since these are often
   document-specific.

   On page 130 of the Biblatex documentation, it lists a ``postnote`` option to the ``\cite{}``
   command, in which the writer can enter in either a numeric page number to refer to, or a
   string that is intended to be directly appended to the line. Find a way to implement this.
   Maybe add a ``postnote`` field to the bibdata entry, and allow that field to be a list in case
   more than one citation uses different page references to the same document?

#. It may be useful for some users to extend the flexibility of the [|] notation to allow nested
   brackets.

#. For people who want to write TeX/LaTeX files in Unicode, but need to deliver an ascii file
   to a journal for their internal processing, maybe you can write a function which does the
   inverse of purify_string(). That is, it converts Unicode characters into their LaTeX
   encoded equivalents. If you work on this, the ``bibtexparser`` module has a good deal of code
   for starting on this.

Python testing to-do
--------------------

#. Add tests for the following::

        options.authorlist_format
        options.editorlist_format
        options.namelist_format

#. Test that trying to import a BibTeX-format BST file generates an ``ImportError`` exception.

#. Test proper formatting of the ``edition`` field.

#. Test for missing fields in entries.

#. The entry ``pagerange1`` has a comma-delimited page range. Currently you don't have a
   template that allows one to differentiate formatting to use ``<pages>`` when there are
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
