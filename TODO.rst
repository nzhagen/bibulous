Python code to-do list: (including goals for version 2.0)
---------------------------------------------------------

The primary goal for version 2.0 is to incorporate integration with a front-end LaTeX package.
For version 1.3, the goal is to have namelist templates working.

- Simplify the get_indexed_variable() function!

- Now that you added three new template variable operators: .upper(), .lower(), .zfill(), and .uniquify(arg),
  update the documentation to show them.

- Is there a way to implement the ``<citealpha>`` variable with templates rather than using an internal 
  special-case function?

- Note that the special template definition::

    author = [<著者名>|<author-en>|]

  never *replaces* the ``author`` field. It only applies this definition if the field is already missing.
  Need to clarify this in the documentation.

- You no longer have functionality using the ``.N`` index (for maximum index). Put that back in?

- If a user added any options blocks to their defined variables, then they may have turned an
  unnested sequence into a nested one. Need to look for that. We can probably do this check
  when the BST file is parsed, rather than when we do string substitution in the template
  for every entry.

- Get ``backrefs`` option back up and working.

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

- Add a test that checks that concatenating operators, like <var.upper().initial()> works.

- Add a test for the new .zfill() operator.

- Add a test for locale-dependent sorting? This requires a lot of work to set up for full
  BIB-AUX-BBL mapping. So it may be best to wait for a more directed test to come along.

- The following should create a malformed implicit loop error but doesn't::

    au = <name.0>, ..., and <name.N.last>

  That is, the first and last elements of the loop must have the same variable structure. Currently 
  the code simply truncates the RHS of the last element and ignores it, but it really should return
  a warning message.

- When I put the line::

    if ('(' in name): print('NAME:', name)

  as the first line inside the function ``initialize_name()``, then in test1 I get::

    NAME: E. (Eric)
    NAME: E. (Eric)
    NAME: E. (Eric)
    NAME: E. (Eric)
    NAME: E. (Eric)
    NAME: E. (Eric)
    NAME: E. (Eric)
    NAME: E. (Eric)
    NAME: E. (Eric)
    NAME: E. (Eric)

  So the question is: why does it go into this initializer 10 (!) times for the same name? I can see it doing
  this once for the sortkey, and then once more for the actual entry, but why 10 times? That might be wasting 
  a huge amount of computational time.

