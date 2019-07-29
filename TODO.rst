Python code to-do list: (including goals for version 2.0)
---------------------------------------------------------

The primary goal for version 3.0 is to incorporate integration with a front-end LaTeX package.
For version 2.1, the goal is to have group templates working.

- Upload the new Python3-compatible code to PyPi.

- The current code apparently only allows defining variables that are all lower case. There is no good reason
  for the restriction, so we should modify the code to allow mixed case.

- If a user added any options blocks to their defined variables, then this may turned an unnested sequence
  into an implicitly nested one. Need to look for that. We can probably do this check
  when the BST file is parsed, rather than when we do string substitution in the template
  for every entry.

- Add a comment in the documentation about changing the option keyword "name_separator" from the default "and"
  to some new one, like "y" (as in Spanish). This appears to force the separator to be used in both the BIB database
  file and not just the output formatted reference. Add functionality allowing you to separate the database name
  separator from the formatted reference name separator.

- It seems likely that the hyperref package compatibility is fragile. Try finding a way to make it more robust.

- Get the ``backrefs`` option back up and working.

- Add stuff from ``jpnbook`` and ``bibtex_items`` in ``/LabNotes/Bibulous/stuff to add to code/``.

- Re-implement the "nameabbrev" field inside ``initialize_name()``. Note that in order to do
  this you will have to re-expand the name into a string first, perform abbrev replacement, and
  then re-convert the result back into the namelist. Here were two items in the testing suite
  that I previously used to use to test this::

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

- Found a way to get different citation labels in the text than in the reference list: use::

    \makeatletter
      \renewcommand{\@biblabel}[1]{}
      \renewcommand{\@cite}[2]{{#1\if@tempswa , #2\fi}}
    \makeatother

  at the top of the ``.tex`` file. Then, in the *text*, LaTeX will use ``citelabel`` while, in the *reference list*,
  it will now ignore the citelabel and simply use the main template without any item label. If we *want* an item label
  for entries in the reference list, then we can simply make them part of the main entrytype template. Will that work
  the way we want? But if we do it with a template, then the reference list item label and the text citation label can
  be treated completely separately.

  Compare this with natbib's author-year style.

- Consider adding a 4-arg operator ``.if_has_substr(input,sub,do_if_true,do_if_false)``.

- Try installing TeXnicCenter (Windows), change its backend to Bibulous, and provide how-to instructions.

- The ``developer_guide.rst`` file has a section "Parsing BST files", but the section has nothing to say about implicit
  loops. It probably should. (At the minimum, point to the location in the docs where implicit loops are discussed.)

- Add templates for: Elsevier journals with numerical
  citations (``elsarticle-num.bst``), Springer journals (``springer.bst``), MNRAS (``mn2e.bst``). Actually, since
  the file ending cannot be used to distinguish Bibulous-format from BibTeX-format style files, maybe we should
  append ``-bibulous`` to each filename? Also, since it's now clear how to define non-numeric citation styles, we
  can start incorporating those as well.

- Implement the GROUP-TEMPLATES section idea. This is a big enough change to bump the version
  number of the codebase, as it would allow bibliographic sections and a much more flexible way
  of manipulating reference lists. The first step here would be to write a wrapper around write_bblfile(),
  and expanding write_bblfile()'s ability (or removing it to the higher level) of turning on/off writing
  of preamble and postambles.

- For every style file you have in the ``templates/`` folder, you should construct an example to put into the
  documentation. Use a standard bibliography database for each, format it with LaTeX, take a screenshot of the
  result, and show.

- Figure out how to get an formatting list of authors like in the following to work::

    Doe, John, David Dane, and Marry Dewy (2000). "This and that". In: Journal of Deep Understanding of Things.

  That is, the first author is given as ``lastname, firstname'' whereas the other authors are given as
  ``firstname lastname``. Probably the answer to this is that the first name in the list should be done outside
  of an implicit loop, while the remaining names should be formatted within the implicit loop.

- Simplify the ``get_indexed_variable()`` function inside ``bibulous.py``.

- Allow direct integration with front-end for: generating glossaries, customizing the
  appearance of citation labels, etc.

- Write a ``bibclean`` function which checks a ``*.bib`` file for errors. Include using
  ``namefield_to_namelist()`` to check for name format errors.

- Common problems in multilanguage files are encoding errors. For this, you can try using
  the Python package ``ftfy``, but this would require introducing into Bibulous an outside
  dependency, and so I'm reluctant to do it without there being an urgent need. Note that
  ``chardet.py`` attempts automatic detection of the encoding of an input file/string.
  That also may come in handy.

- Implement a bibliography format in which repeated duplicates of author names are replaced
  with a long dash. (Or ``\textit{idem}`` instead of the dash.)

- ``get_edition_ordinal()``, as currently implemented, will only work for English-language
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

- Change the way you define the "specials" to use an object-oriented accessor. That is, do not
  generate a field until it is asked for. This should speed things up significantly when the
  user has specials defined.

- Create a checklist for developers to make sure that they have done everything necessary to
  check in new code:
    - [Developer] ran the tests and they passed!
    - Someone else ran the tests and they passed!
    - A computer ran the tests automatically and they passed! (Continuous Integration)
    - The code formatting guidelines are met.
    - The code coverage didn't decrease (i.e. the testing suite still test most of the code base).
    - Changes were described in a ChangeLog.
    - Commit messages make sense.

- ``citationstyles.org`` has thousands of styles defined which are used by other programs such
  as Zotero and Mendeley. Think about how to convert these to Bibulous templates and have a large
  library of pre-defined styles. PS: Also see ``https://github.com/citation-style-language``

- Add an example that handles the question posted at http://tex.stackexchange.com/questions/961/bibtex-style-that-groups-by-author


Python testing to-do
--------------------

- Add a test for the new operators: ``.if_str_equal()``, ``.if_num_equals()``, ``.if_less_than()``, ``.if_greater_than()``, and
  ``.null()``.

- The following should create a malformed implicit loop error but doesn't::

    au = <name.0>, ..., and <name.N.last>

  That is, the first and last elements of the loop must have the same variable structure. Currently
  the code simply truncates the RHS of the last element and ignores it, but it really should return
  a warning message.

- Add a test for locale-dependent sorting? This requires a lot of work to set up for full
  BIB-AUX-BBL mapping. So it may be best to wait for a more directed test to come along.

- Add a test for ``.uniquify(1)`` and ``.uniquify(a)``.

- Add a test for the ``.N`` functionality inside the implicit loops.

- Add a test for implicit loops where you have stuff in front of the implicit loop and behind it, within
  the same variable definition. It should work. Especially try something like
  ``au = [<authorname.0>, ...,{ and }<authorname.6>]`` to see if you can put option brackets around the
  entire loop.
