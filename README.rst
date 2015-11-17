=================
Bibulous Overview
=================

Bibulous is a drop-in replacement for BibTeX that makes use of style templates instead of BibTeX's BST language. The code is written in Python and, like BibTeX itself, is open source.

Bibulous developed out of frustration with the complexity of creating bibliography styles using BibTeX's obscure language, and also from the realization that because bibliographies are highly structured, one should be able to specify them simply and flexibly using a template approach. There should be no need to learn a new language just to build a bibliography style, and specifying a style should take only a matter of minutes.

Bibulous incorporates this template approach, and at the same time implements many of the modern enhancements to BibTeX, such as the ability to work with languages other than English, better support for allowing non-standard bibliography entry types, increased options for author name formatting, and more. And one can use the same basic structures and LaTeX commands to generating each of: a bibliography, a glossary, an annotated bibliography, a list of acronyms and symbols, and more, by specifying a different style template for each case.

Bibulous' “style template” files allow a user to visualize the entire bibliography format structure in a concise way within a single page of text. Moreover, the template is structured with its own Python-like mini-language, intended to allow uses to create flexible formatting instructions quickly and easily. The example below illustrates the simplicity of the format.

The project website, with complete documentation, can be found at `<http://nzhagen.github.io/bibulous/>`_. The complete sourcecode for the project can be found at `<https://github.com/nzhagen/bibulous>`_. For any questions, the Bibulous project maintainer can be contacted at `and.the.light.shattered@gmail.com <mailto:and.the.light.shattered@gmail.com>`_.

Installation
============

Installing using pip:::

   pip install bibulous

Instructions for installing Bibulous, and for seamlessly integrating it into your normal LaTeX workflow, are given in the `getting started <https://github.com/nzhagen/bibulous/blob/master/doc/getting_started.rst>`_ section.
Users can also consult the `guidelines for writing style templates <https://github.com/nzhagen/bibulous/blob/master/doc/guidelines_for_writing_style_templates.rst>`_ for further information, and the `examples <https://github.com/nzhagen/bibulous/blob/master/doc/examples.rst>`_ section. A `FAQ <https://github.com/nzhagen/bibulous/blob/master/doc/faq.rst>`_ page is also available.

Another approach is to clone the git repository `<https://github.com/nzhagen/bibulous>`_ and place it into your Python path.
For compiling bibliographies, the only file needed within the project is ``bibulous.py``, so that going to `<https://github.com/nzhagen/bibulous>`_ and copying `bibulous.py <https://github.com/nzhagen/bibulous/raw/master/bibulous.py>`_ from there is sufficient.

Example
=======

For a very simple bibliography, consisting of only journal articles and books, a complete style template file may consist of just two lines:::

   article = <au>, \enquote{<title>,} \textit{<journal>} \textbf{<volume>}: ...
                [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).[ <note>]
   book = [<au>|<ed>|], \textit{<title>} (<publisher>, <year>)...
                [, pp.~<startpage>--<endpage>].[ <note>]

The ``<variable>`` notation indicates that the corresponding bibliography entry's field is to be inserted into the template there. The ``[...|...]`` notation behaves similar to an if...elseif... statement, checking whether a given field is defined within the bibliography entry. If not defined, then it attempts to implement the instruction in the block following the next ``|`` character.

We can read the above article template as indicating the following structure for LaTeX-formatting the cited entry in the bibliography (``.bib`` file). For articles, we first insert the list of author names (formatted according to the default form), followed by a comma. If no ``author`` field was found in the bibliography entry, then insert ``???`` to indicate a missing required field. Next insert a quoted title, followed by an italicized journal name, and a boldface volume number (all of these are required fields). Next, if the ``pages`` field was found in the entry's database, then parse the start and end page numbers and insert them here. If the ``pages`` field indicates that there was only one page, then use that instead. Or if the ``pages`` field is not present, then check to see if the ``eid`` is defined, and use it instead. However, if none of these three possibilities are available, then insert the “missing field” indicator, ``???``. Finally, put the year inside parentheses, and if the ``note`` field is defined in the entry, then add that to the end (following the period). If ``note`` is not defined, then just ignore it.

One can read the book template similarly, and find that it has different required and optional fields. The simplicity of the format allows one to customize databases to suit any use. For example, to use a bibliography entrytype ``本`` instead of ``book``, then all that is necessary is to go into the template file and change ``book`` to ``本``. If a user wishes to add a new field, such as ``translator``, then if it has been added to the ``.bib`` database file, then all that is needed is to add some text to the template, such as ``(<translator>, trans.)`` to insert the field into every bibliography entry that has ``translator`` defined for that entrytype.

Developers
==========

Bibulous is a new project, and so it has until now been a solo effort. Anyone interested in helping out is welcome to join; just send an email to the developers mailing list and we will try to help you get involved and show you the ropes. And, this being the maintainer's first open source project, any suggestions by experienced developers are welcome.

Guidelines for developers are given in `developer_guide.rst <https://github.com/nzhagen/bibulous/blob/master/doc/developer_guide.rst>`_, and includes an overview of the project's strategy and overall code structure. Note that a bug tracking system has not yet been set up for the project. HTML-based documentation is provided at ``bibulous/doc/_build/html/index.html``, and a corresponding PDF file at `bibulous/doc/_build/latex/Bibulous.pdf <https://github.com/nzhagen/bibulous/blob/master/doc/_build/latex/Bibulous.pdf>`_. The `setup.py <https://github.com/nzhagen/bibulous/blob/master/setup.py>`_ and `MANIFEST.in <https://github.com/nzhagen/bibulous/blob/master/MANIFEST.in>`_ files provided in the repository base directory are used to create a Python package using the ``disutils`` distribution utilities module.

Contact
=======

For any questions, the current Bibulous project maintainer can be reached at `and.the.light.shattered@gmail.com <mailto:and.the.light.shattered@gmail.com>`_.

License
=======

Bibulous is released under the MIT/X11 license, meaning that it is free and open source, and that it can be used without restriction in other programs, commercial or not. The full license is given in the file `LICENSE.txt <https://github.com/nzhagen/bibulous/blob/master/LICENSE.txt>`_.
