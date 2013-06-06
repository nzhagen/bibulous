Bibulous
========

Bibulous is a drop-in replacement for BibTeX that makes use of style templates instead of BibTeX's
BST language. The code is written in Python and, like BibTeX itself, it is open source.

Bibulous developed out of frustration with developing bibliography styles using BibTeX's obscure
style file language, and from the realization that bibliographies are highly structured, so that
they can be specified simply and flexibly using a template approach. With templates, one can
develop entirely new bibliography styles in a matter of minutes, and often without having to refer
to the user manual during the entire process.

At the same time, Bibulous incorporates a lot of the modern enhancements to BibTeX, such as the
ability to work with languages other than English, better support for allowing non-standard
bibliography entry types, functionality for enhanced citation styles, and increased options for
author name formatting, among others.

Bibulous' "style template" files allow a user to visualize the entire bibliography format
structure in a concise way within a single page of text. Moreover, the template is structured with
its own mini-language, intended to allow uses to create flexible formatting instructions quickly
and easily. The example below illustrates the simplicity of the format.

Example
-------

For a very simple bibliography, consisting of only journal articles and books, a style template
file might only consist of just two lines::

   article = <authorlist>, ``<title>,'' \textit{<journal>} \textbf{<volume>}: [<startpage>--<endpage>|<startpage>|<eid>|] (<year>).[ <note>]
   book = [<authorlist>|<editorlist>|], \textit{<title>} (<publisher>, <year>)[, pp.~<startpage>--<endpage>].[ <note>]

The ``[...|...]`` notation behaves similar to an if...elseif statement, while the ``<variable>``
notation indicates that the field mapping to that variable name is to be inserted into the
template there. And we can read the article template as indicating the following bibliography
format: For articles, we first insert the list of author names (formatted according to the default
form). If no ``author`` field was found in the bibliography entry, then insert ``???`` to indicate
a missing required field. Next insert a quoted title, followed by an italicized journal name, and
a boldface volume number (all required. Next, if the ``pages`` field was found in the entry's
database, then parse the start and end page numbers and insert them here. If the ``pages`` field
indicate that there was only one page, then use that instead. Or if the ``pages`` field is not
present, then check to see if the ``eid`` is defined, and use it instead. However, if none of
these three possibilities are available, then insert the "missing field" indicator ``???``.
Finally, put the year inside parentheses, and if the ``note`` field is defined in the entry, then
add that to the end (following the period). If ``note`` is not defined, then just ignore it.

One can read the ``book`` template similarly, and find that it has different required and optional
fields. The simplicity of the format allows one to customize databases to suit any use. For
example, to use an entrytype ``<?>`` instead of ``<book>``, then all that is necessary is to go
into the template file and change ``<book>`` to ``<?>``. Of, if you wish to add a new field, such
as ``translator``, then if it has been added to the ``.bib`` database file, one need only add some
text to the template, say ``[(: <translator>) ]`` to insert that into every bibliography entry
which has ``translator`` defined for that entrytype.

Installing and instructions
---------------------------

Instructions for installing Bibulous, and for seamlessly integrating it into your normal LaTeX
workflow, are given in the ``INSTALL.rst`` file. Users can also consult the user guide
(``user_guide.rst``) for further information and tutorials. A FAQ page is also available.

Developers
----------

Bibulous is a brand new project, and so it has so far been a solo effort. Anyone interested in
helping out is welcome to join; just send an email to the developers mailing list and we will try
to help you get involved and show you the ropes. And, this being the maintainer's first open
source project, any suggestions by experienced developers are welcome.

Guidelines for developers are given in ``developer_guide.rst``, and includes an overview of the
project's strategy and overall code structure. Note that a bug tracking system has not yet been
set up for the project.

License
-------

Bibulous is released under the MIT/X11 license, meaning that it is free and open source, and that
it can be used without restriction in other programs, commercial or not. The license is given in
the file ``LICENSE.txt``, the text of which is reproduced below.

Copyright (c) 2013 Bibulous developers

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:The above copyright notice and this
permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
