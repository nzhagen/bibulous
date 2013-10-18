Python code to-do list: (including goals for version 2.0)
---------------------------------------------------------

The primary goal for version 2.0 is to incorporate integration with a front-end LaTeX package.
For version 1.3, the goal is to have namelist templates working.

- Once you have the new namelist templates in, remove all the unnecessary keyword options from
  the testing suite template files and the ``templates`` folder files as well.

- Add a ``.sentence_case()`` function inside template variables, so you can use it on ``<title>``
  like ``<title.sentence_case()>``. Maybe another function ``.ordinal()`` can be used to convert
  the edition number into an ordinal too. Maybe ``.monthname()`` and ``.monthabbrev()`` too?

- If a user added any options blocks to their defined variables, then they may have turned an
  unnested sequence into a nested one. Need to look for that. We can probably do this check
  when the BST file is parsed, rather than when we do string substitution ni tehe template
  for every entry.

- Rewrite the ``Overall project strategy and code structure`` section of
  ``developer_guide.rst`` to take into account the new program flow.

- Get ``backrefs`` option back up and working.

- Get ``nameabbrev`` back up and working.

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

- Currently, the ``enwrap_nested_quotes()`` function only works for the American convention
  of quotation. Adapt to the British convention and, even better, for universal quotation
  usage.

- Re-implement the "nameabbrev" field inside ``initialize_name()``. Note that in order to do 
  this you will have to re-expand the name into a string first, perform abbrev replacement, and 
  then re-convert the result back into the namelist, in order for this to work here. Here were
  two items in the testing suite that I used to use to test this::

    %% Test sorting with an entry using a "nameabbrev" field.
    @ARTICLE{Fontaine1234,
    author = {Jean de la Fontaine du Bois Joli},
    title = {Something},
    year = {1234},
    nameabbrev = {Jean de la Fontaine > {JdlF.}}
    }

    %% The only difference between this entry and the one above, except for the entrykey, is in "nameabbrev".
    @ARTICLE{Fontaine1234a,
    author = {Jean de la Fontaine du Bois Joli},
    title = {Something},
    year = {1234},
    nameabbrev = {de la Fontaine > {dlF.}, du Bois > du}
    }




Python testing to-do
--------------------

- Add a test for locale-dependent sorting? This requires a lot of work to set up for full
  BIB-AUX-BBL mapping. So it may be best to wait for a more directed test to come along.

- Test that Bibulous prints a warning message, and does not emit an exception, when the
  AUX file contains a citation key that does not exist in the database.

- Need to add a test for the ``<...>`` are properly formed in the template strings. For example,
  if by mistake a user types ``<year|<number>`` then the template will be malformed, but Bibulous
  doesn't return an error. It will think that ``year|<number`` is a single variable name.

- Make sure that hyphenated names are corrected formatted to hyphenated initials.

- Check that a BIB file entry whose author field ends in "and others" is translated correctly into
  \textit{et al.} in the BBL file.

- The following template definition should produce an error/warning::

    <[<authorlist.0.first> ][<authorlist.0.middle.initial()>. ][<authorlist.0.prefix> ]<authorlist.0.last>[, <authorlist.0.suffix>]>

  but currently doesn't.

- The following should create a malformed implicit loop error but doesn't::

    authorliststr = <name.0>, ..., and <name.N.last.initial()>

  That is, the first and last elements of the loop must have the same variable structure. Currently 
  the code simply truncates the RHS of the last element and ignores it, but it really should return
  a warning message.

