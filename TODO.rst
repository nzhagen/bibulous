Python code to-do list: (including goals for version 2.0)
---------------------------------------------------------

The primary goal for version 2.0 is to incorporate integration with a front-end LaTeX package.

- Rewrite the ``Overall project strategy and code structure`` section of
  ``developer_guide.rst`` to take into account the new program flow.

- Get ``backrefs`` option back up and working.

- Add _templates_ for name formatting (to generate ``authorliststr`` and ``editorliststr`` from
  the ``author`` and ``editor`` fields, for example).

- Allow direct integration with front-end for: generating glossaries, customizing the
  appearance of citation labels, etc.

- Look into whether the code can be simplified and user scripts still benefit if you move some
  bibulous module functions from module scope functions to Bibdata class methods.

- Write a ``bibclean`` function which checks a ``*.bib`` file for errors. Include using
  ``namefield_to_namelist()`` to check for name format errors.

- Common problems in multilanguage files are encoding errors. For this, you can try using
  the Python package ``ftfy``, but this would require introducing into Bibulous an outside
  dependency, and so I'm reluctant to do it without there being an urgent need. Note that
  ``chardet.py`` attempts automatic detection of the encoding of an input file/string.
  That also may come in handy.

- Implement a bibliography format in which repeated duplicates of author names are replaced
  with a long dash. (Or ``\textit{idem}`` instead of the dash.)

- ``format_edition()``, as currently implemented, will only work for English-language
  bibliographies. This needs to be modified so that it can be made multilingual. This is actually
  even more difficult than it sounds, since many languages actually use gender-dependent
  ordinals, so that knowing the number alone is not sufficient.

- For people who want to write TeX/LaTeX files in Unicode, but need to deliver an ascii file
  to a journal for their internal processing, maybe you can write a function which does the
  inverse of ``purify_string()``. That is, convert Unicode characters into their LaTeX-
  encoded equivalents. If you work on this, the ``bibtexparser`` module has a good deal of code
  for starting on this.


Python testing to-do
--------------------

- Add a test for locale-dependent sorting? This requires a lot of work to set up for full
  BIB-AUX-BBL mapping. So it may be best to wait for a more directed test to come along.

- Test that Bibulous prints a warning message, and does not emit an exception, when the
  AUX file contains a citation key that does not exist in the database.

- Need to add a test for the ``<...>`` are properly formed in the template strings. For example,
  if by mistake a user types ``<year|<number>`` then the template will be malformed, but Bibulous
  doesn't return an error. It will think that ``year|<number`` is a single variable name.
