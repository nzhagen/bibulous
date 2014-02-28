Python code to-do list: (including goals for version 2.0)
---------------------------------------------------------

The primary goal for version 2.0 is to incorporate integration with a front-end LaTeX package.
For version 1.4, the goal is to have group templates working.

- Add a test for the new ``##:##`` indexer format.

- We seem to have duplicate special variables ``citekey`` and ``entrykey``. What's up with that?

- Add a test using the following special template: 
  ``author_or_editor = [[[<authorlist.0.prefix>]<authorlist.0.last>]|[[<editorlist.0.prefix>]<editorlist.0.last>]]``.
  This is a good test for allowing nested templates.

- Note that while the special-template ``au = <authorname.0>, ...,{ and }<authorname.6>`` works fine, the
  special-template ``au = [<authorname.0>, ...,{ and }<authorname.6>]`` does *not*. The code treats the final
  square bracket as part of the implicit loop, and not as a signature of an optional template block. Fix that!

- Implement the GROUP-TEMPLATES section idea. This is a big enough change to bump the version
  number of the codebase, as it would allow bibliographic sections and a much more flexible way
  of manipulating reference lists. The first step here would be to write a wrapper around write_bblfile(),
  and expanding write_bblfile()'s ability (or removing it to the higher level) of turning on/off writing
  of preamble and postambles.

- Add the operator .uniquify(arg) to the documentation?

- Is there a way to implement the ``<citealpha>`` variable with templates rather than using an internal 
  special-case function?

- For every style file you have in the ``templates/`` folder, you should construct an example to put into the
  documentation. Use a standard bibliography database for each, format it with LaTeX, take a screenshot of the
  result, and show.

- Figure out how to get an formatting list of authors like in the following to work::

  Doe, John, David Dane, and Marry Dewy (2000). "This and that". In: Journal of Deep Understanding of Things.

  That is, the first author is given as ``lastname, firstname'' whereas the other authors are given as 
  ``firstname lastname``.

- In the get_names() function, you've hard-coded the "authorname" and "editorname" variables. Users should be
  able to whatever names they like. Fixing this is harder than it looks at first glance! How to inform a given
  template which namelist to query, when all it knows locally is the template string and not the actual field?

- Simplify the ``get_indexed_variable()`` function inside ``bibulous.py``!

- You no longer have functionality using the ``.N`` index (for maximum index). Put that back in.

- If a user added any options blocks to their defined variables, then they may have turned an
  unnested sequence into a nested one. Need to look for that. We can probably do this check
  when the BST file is parsed, rather than when we do string substitution in the template
  for every entry.

- Get the ``backrefs`` option back up and working.

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

- The following entry (using ``and others`` in the author field) did not get correctly converted to an
  *et al.* ending to the formatted author list::

    @Misc{Arp2004,
    title = {An open letter to the scientific community},
    year = {2004},
    author = {Halton Arp and others}
    }

- Add a test for locale-dependent sorting? This requires a lot of work to set up for full
  BIB-AUX-BBL mapping. So it may be best to wait for a more directed test to come along.

- The following should create a malformed implicit loop error but doesn't::

    au = <name.0>, ..., and <name.N.last>

  That is, the first and last elements of the loop must have the same variable structure. Currently 
  the code simply truncates the RHS of the last element and ignores it, but it really should return
  a warning message.
