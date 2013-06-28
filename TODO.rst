Python code to-do list
----------------------

#. (a) give instructions to users about how to overwrite the
   generate_sortkey() function; (b) make a function generate_bibitem_tag() --- which can also
   be overwritten by a user-defined function --- that generates the bibitem tag.

#. Look into whether the code can be simplified and user scripts still benefit if you move some
   bibulous module functions from module scope functions to Bibdata class methods.

#. Write a ``bibclean`` function which checks a ``*.bib`` file for errors. Include using
   ``namefield_to_namelist()`` to check for name format errors.

#. Common problems in multilanguage files are encoding errors. For this, you can try using
   the Python package ``ftfy``, but this would require introducing into Bibulous an outside
   dependency, and so I'm reluctant to do it without there being an urgent need.

#. Implement a bibliography format in which repeated duplicates of author names are replaced
   with a long dash. (Or ``\textit{idem}`` instead of the dash?)

#. Currently Arabic prefixes of names, like al-Turabi, will produce a space between the ``al-``
   and the last name. Need to fix. Or maybe just let users make their own template script to
   handle that case?

#. ``format_edition()``, as currently implemented, will only work for English-language
   bibliographies. This needs to be modified so that it can be made multilingual. This is actually
   even more difficult than it sounds, since many languages actually use gender-dependent
   ordinals, so that knowing the number alone is not sufficient.

#. It may be useful for some users to extend the flexibility of the [|] notation to allow nested
   brackets.

#. For people who want to write TeX/LaTeX files in Unicode, but need to deliver an ascii file
   to a journal for their internal processing, maybe you can write a function which does the
   inverse of purify_string(). That is, it converts Unicode characters into their LaTeX
   encoded equivalents. If you work on this, the ``bibtexparser`` module has a good deal of code
   for starting on this.

Python testing to-do
--------------------

#. Add a test for locale-dependent sorting.

Template files to-do
--------------------

#. Try implementing some other BST formats, especially OSA's Opt. Lett. and SPIE's Opt. Eng.
   Note that ``chicago.sty`` uses ``chicago.bst``, and ``apalike.sty`` uses ``apalike.bst``.
