Examples
********

Example 1
=========

The following example is taken from a question posted at ``http://tex.stackexchange.com/questions/147675/bibtex-scientific-style-with-pages-at-the-end``, where the desired bibliography format is given as:

.. image:: _static/example1a.png
   :width: 50%

With Bibulous, we can easily provide templates that provide the formatting that the OP asks for:

.. literalinclude:: ../examples/example1.bst

so that if we use this template together with the following database file:

.. literalinclude:: ../examples/example1.bib

then we get the formatted result shown below

.. image:: _static/example1b.png
   :width: 60%

************************************************

Example 2
=========

The next example is taken from the bibliography style found in: Dimitri Mihalas and James Binney, _Galactic Astronomy: Structure and Kinematics_, 2nd ed. (W. H. Freeman, New York, 1981). A snapshot from the the book's bibliography looks like

.. image:: _static/example2a.png
   :width: 60%

To produce this style, we can define the following templates:

.. literalinclude:: ../examples/example2.bst

so that with the following database file:

.. literalinclude:: ../examples/example2.bib

we get the following formatted result

.. image:: _static/example2b.png
   :width: 60%

************************************************

Example 3
=========

The next example illustrates the style used by the Optical Society of America (OSA) for their journals. The following formatted bibliography

.. image:: _static/example3.png
   :width: 60%

is obtained using the template

.. literalinclude:: ../examples/example3.bst

and the database file

.. literalinclude:: ../examples/example3.bib

************************************************

Example 4
=========

The next example illustrates the style used by the society SPIE for their journals. The following formatted bibliography

.. image:: _static/example4.png
   :width: 60%

is obtained using the template

.. literalinclude:: ../examples/example4.bst

and the database file

.. literalinclude:: ../examples/example4.bib

************************************************

Example 5
=========

The following example is taken from a question posted at ``http://tex.stackexchange.com/questions/160737/bold-labels-and-more-with-custom-bibtex-bst-and-author-year``, where an answer to the original poster's question is given as

.. image:: _static/example5a.png
   :width: 60%

That is the reference list entries should have the author list in bold, journal articles should have their title quoted using German-style quotation marks, and editor lists should be given in small caps. The first answerer to the OP's question gives an example database file 

.. literalinclude:: ../examples/example5.bib

that makes use of separate formatting instructions for titles and subtitles, so that an appropriate style template is

.. literalinclude:: ../examples/example5.bst

producing the formatted result

.. image:: _static/example5b.png
   :width: 60%

************************************************

Example 6
=========

The following example is taken from a question posted at ``http://tex.stackexchange.com/questions/147932/peerage-titles-in-the-author-field-in-bibtex``. The question's answerer responds with a Biblatex solution, in which ``nameaddon`` and ``shortauthor`` fields are added to the ``*.bib`` database file, as in

.. literalinclude:: ../examples/example6.bib

The formatting template makes use of these additional fields, and provides a citation label using the ``shortauthor`` field's first three characters followed by the last two characters in the ``year`` field:

.. literalinclude:: ../examples/example6.bst

The formatted result looks like

.. image:: _static/example6.png
   :width: 60%

************************************************

Example 7
=========

The following example is taken from a question posted at ``http://tex.stackexchange.com/questions/145038/some-citation-numbers-in-bold-others-not/168233#168233``, where the OP asks if there is a way to have some citations given in **bold** font. This can be achieved with a user-defined script, as shown below. With tha database file

.. literalinclude:: ../examples/example7.bib

and the style template file

.. literalinclude:: ../examples/example7.bst

we can make use of a simple main ``.tex`` file

.. literalinclude:: ../examples/example7.tex

to produce a formatted result

.. image:: _static/example7.png
   :width: 60%

************************************************

Example 8
=========

The following example is taken from a question posted at ``http://tex.stackexchange.com/questions/169300/modify-plain-bst-file/172828#172828``, where the OP asks for a way to customize the formatted reference list so that the first line contains the author names and date, while the second and subsequent lines are given a hanging indent. This can be achieved with the following setup. With the database file

.. literalinclude:: ../examples/example8.bib

and the style template file

.. literalinclude:: ../examples/example8.bst

we can make use of a simple main ``.tex`` file

.. literalinclude:: ../examples/example8.tex

to produce a formatted result

.. image:: _static/example8.png
   :width: 60%

************************************************

Example 9
=========

The following example is taken from a question posted at ``http://tex.stackexchange.com/questions/172444/suppress-month-and-day-for-journal-articles-and-maintain-for-a-newspaper-article``, where the OP asks for a way to create a reference list in which newspaper articles have the month and day of publication shown while journal articles do not. The cleanest way of implementing this in Bibulous is simply to use a different entrytype for newspaper articles and journal articles, as shown below. For this example, we have a database file

.. literalinclude:: ../examples/example9.bib

and a style template file

.. literalinclude:: ../examples/example9.bst

that when compiled by the main ``.tex`` file

.. literalinclude:: ../examples/example9.tex

produces the formatted result

.. image:: _static/example9.png
   :width: 60%

************************************************

Example 10
==========

The following example is taken from a question posted at ``http://tex.stackexchange.com/questions/68080/beamer-bibliography-icon?lq=1``, where the OP asks for a way to place images alongside each bibliography entry. For this example, we have a database file

.. literalinclude:: ../examples/example10.bib

and a style template file

.. literalinclude:: ../examples/example10.bst

that when compiled by the main ``.tex`` file

.. literalinclude:: ../examples/example10.tex

produces the formatted result

.. image:: _static/example10.png
   :width: 60%











************************************************

Example ?
=========

This follows an online question posted at ``http://tex.stackexchange.com/questions/961/bibtex-style-that-groups-by-author``.
