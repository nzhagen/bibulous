Developer guide
***************

Guidelines for Python coding style
==================================

1. Note that you can mix 8-bit Python strings (ASCII text) with UTF-8 encoded text as long as the 8-bit string contains only ASCII characters.

2. Keep in mind when running into Unicode errors: reading a line of text from a file produces a line of bytes and not characters. To decode the bytes into a string of characters, you need to know the encoding.

3. There are a couple of minor points where the Bibulous coding standards deviates from Python's PEP8:

    (a) A line width of 100 is the standard (not 80).
    (b) In general, statements that evaluate to a boolean are placed within parentheses (i.e. ``if (a < b):`` rather than ``if a < b:``).

4. Many developers prefer to spread out code among a large number of small files. Bibulous is currently organized in the opposite fashion -- all of the code needed to run ``bibulous`` to create a ``.bbl`` file is located within a single large file. Several auxiliary scripts exist, but these use ``bibulous.py`` as a core library file, and perform different tasks (such as extracting sub-bibliography databases) than the main file was designed to do.

Overall project strategy and code structure
===========================================

The basic function of BibTeX is to accept an ``.aux`` file as input and to produce a ``.bbl`` file as output. The ``aux`` file contains all of the citation information as well as the filenames for the bibliography database file (``.bib``) and the style file (``.bst``).

The basic program flow is as follows:

    1. Read the .aux file and get the names of the bibliography databases (.bib files), the style templates (.bst files) to use, and the entire set of citations.
    2. Read in all of the bibliography database files into one long dictionary (`bibdata`), replacing any abbreviations with their full form. Cross-referenced data is *not* yet inserted at this point. That is delayed until the time of writing the BBL file in order to speed up parsing.
    3. Read in the Bibulous style template file as a dictionary (`bstdict`).
    4. Now that all the information is collected, go through each citation key, find the corresponding entry key in `bibdata`. If there is crossref data, then fill in missing values here. Also create the "special fields" here. Finally, from the entry type, select a template from `bstdict` and begin inserting the variables one-by-one into the template.

Because the ``.bib`` file is highly structured, it is straightforward to write a parser by hand in Python: the ``parse_bibfile()`` method converts the ``.bib`` file contents into a Python dictionary (the ``Bibdata`` class' ``bibdata``). The ``.aux`` file is even easier to parse, and the ``parse_auxfile()`` method converts the citation information into the ``Bibdata`` class' ``citedict`` dictionary. The ``.bst`` style template file, having its own domain specific language, is much more complicated, so that its parser is generated from a grammar written for the ``Antlr`` parser generator. (This creates Bibulous' only external dependency -- Java -- which we may be able to eliminate if we use a Python-based parser generator, such as ``pyparsing``.)

The ``Bibdata`` class thus holds all relevant information needed to operate on a bibliography and generate the output LaTeX-formatted ``.bbl`` file.

Parsing BIB files
=================

parse_bibfile()
---------------

The strategy for ``parse_bibfile()`` is to find each individual bibliography entry, determine its entry type, and save all of the text between the entry's opening and closing braces as one long string, to be passed to ``parse_bibentry()`` for parsing. To gather the entry data string, we first look for the next line that starts with ``@``. On that line, we look for a string after the ``@`` followed by ``{``, where the string gives the entry type. After we know the entry type, we look for the corresponding closing brace. If we don't find it on the same line, then we read in the next line, and so forth, concatenating all of the lines into one long "entry string" until we encounter the corresponding closing brace. Once we have this extended "entry string" we feed it to ``parse_bibentry()`` to generate the bibliography data. Once we have come to the end of a given entry, we continue reading down the file looking for the next '@' and so on.

Although this approach effectively means that we have to pass twice through the same data, dealing with brace-matching can otherwise become a mess since the BibTeX format, since it allows nested delimiters, is not directly compatible with regular expressions.

parse_bibentry()
----------------

``parse_bibentry()`` only needs to worry about a single entry, and there are four possible formats for the entry string passed to the function:

    1. If the entrytype is a comment, then skip everything, adding nothing to the database dictionary.
    2. If the entrytype is a preamble, then treat the entire entry contents as a single fieldvalue. Append the string onto the ``preamble`` value in the ``bibdata`` dictionary.
    3. If the entrytype is a ``string`` (i.e. an abbreviation), then there is no entrykey. Get the fieldname (abbreviation key), and the remainder of the string is a single field value (the full form of the abbreviated string. Add this key-value pair to the ``abbrevs`` dictionary.
    4. If the entry is any other type, then get the entrykey, and the remainder of the string is a *series* of field-value pairs.

Once it determines which of these four options to use, ``parse_bibentry()`` extracts the entry key (if present), separates out each of the fields (if more than one is present) and loops over each field with a call to ``parse_bibfield()`` to extract the field key-value pairs.

parse_bibfield()
----------------

``parse_bibfield()`` is the workhorse function of the BIB parsing. And because of BibTeX's method for allowing concatenation, use of abbreviation keys, and use of two different types of delimiters (``"..."`` or ``{...}``), this function is a little messy. However, for the format of a given field, there are four parsing possibilities:

    1. If the field begins with a double quote ``"`` then scan until you find the next ``"``. Add that to the result string. If the ending ``"`` is followed by a comma, then the field is done; return the result string. If the ending is followed by a ``#`` then expect another field string. Scan for it and append it to the current result string.
    2. If the field begins with ``{`` then scan until you resolve the brace level. This should be followed by a comma, since no concatenation is allowed of brace-delimited fields. Otherwise issue a syntax error warning.
    3. If the field begins with a ``#`` (concatenation operator) then skip whitespace to the next character set, where you should expect a quote-delimited field. Append that to the current result string.
    4. If the field begins with anything else, then the substring up until the first whitespace character represents an abbreviation key. Locate it and substitute it in. If you don't find the key in the ``abbrevs`` dictionary, give a warning and skip.

Parsing AUX files
=================

The ``.aux`` file contains the filenames of the ``.bib`` database file and the ``.bst`` style template file, as well as the citations. The ``get_bibfilenames()`` method scans through the ``.aux`` file and locates a line with ``\bibdata{...}`` which contains a filename or a comma-delimited list of filenames, giving the database files. Another line with ``\bibstyle{...}`` gives the filename or comma-delimited list of filenames for style templates. The filenames obtained are saved into the ``filedict`` attribute -- a dictionary whose keys are the file extensions ``aux``, ``bbl``, ``bib``, ``bst``, or ``tex``.

The ``parse_auxfile()`` method makes a second pass through the ``.aux`` file, this time looking for the citation information. (Auxiliary files are generally quite small, so taking multiple passes through them cost very little time.) Each line with ``\citation{...}`` contains a citation key or comma-delimited list of citation keys -- each one is added into the citation dictionary (``citedict``), with a value corresponding to the citation order.

Parsing BST files
=================

(This part is changing at the moment, and so the documentation is not available yet.)

Writing the BBL file
====================

Now that all the information is available to Bibulous, we can begin writing the output BBL file. First we write a few lines to the preamble, including the ``preamble`` string obtained from the ``.bib`` database files. Next we create the citation list -- the citations listed in the sorting order as defined in the style template files. (This requires a surprising amount of code to get right -- see **Generating sortkeys** below.) We loop over each citation in the desired order, and insert cross-reference information to fill in missing fields, and parse each name field (see the "Formatting names" subsection below). The cross-referencing and name parsing steps can be delayed until later on in the processing chain, but would require more complex code to do there, so doing them here keeps the code simpler without sacrificing much speed. (The assumption here is that the citation list is small, at least in comparison to the database, so that limiting the difficult parsing to only those entries cited will allow significant improvement in speed.) Finally, at each step in the loop, we call ``format_bibitem()`` to insert the database entry fields into the appropriate style template, incorporating any extra formatting requested by the user in the style template file.

Name formatting
================

One of the more complex tasks needed for parsing BIB files is to resolve the elements of name lists (typically saved in the ``author`` and ``editor`` fields). In order to know how these should be inserted into a template, it is necessary to know which parts of a given person's name correspond to the first name, the middle name(s), the "prefix" (or "von part"), the last name (or "surname"), and the "suffix" (such as "Jr." or "III"). These five pieces or each person's name are saved as a dictionary, so that a bibliography entry with five authors is represented in ``<authorlist>`` as a list of five dictionaries, and each dictionary having keys ``first``, ``middle``, ``prefix``, ``last``, and ``suffix``.

In order to speed up parsing times, the actual mapping of the ``author`` or ``editor`` fields to ``authorlist`` or ``editorlist`` is not done until the loop over citation keys performed while writing out the BBL file. The function that product the list-of-dicts parsing result is ``namestr_to_namedict(namestr)``.

The default formatting of a namelist into a string to be inserted into the template is performed by ``format_namelist()``.

create_namelist()
-----------------

A BibTeX "name" field can consist of three different formats of names:

    1. A space-separated list: ``[firstname middlenames suffix lastname]``
    2. A two-element comma-separated list: ``[prefix lastname, firstname middlenames]``
    3. A three-element comma-separated list: ``[prefix lastname, suffix, firstname middlenames]``

So, an easy way to separate these three categories is by counting the number of commas that appear. The trickiest part here is that although we can use ``and`` as a name separator, we are only allowed to do so if ``and`` occurs at the top brace level.

In addition, in order to make name parsing more flexible for nonstandard names, Bibulous adds two more name formats to this list:

   4. A four-element comma-separated list: ``[firstname, middlenames, prefix, lastname]``
   5. A five-element comma-separated list: ``[firstname, middlenames, prefix, lastname, suffix]``

For each name in the field, we parse the name tokens into a dictionary. We then compile all of the dictionaries into a list, ordered by the appearance of the names in the input field.

format_namelist()
-----------------

Given a namelist (list of dictionaries), we glue the name elements together into a single string, incorporating all of the format options selected by the user in the template file. This includes calls to ``namedict_to_formatted_namestr()``, and to ``initialize_name()`` if converting any name tokens to initials.

Generating sortkeys
===================

If the user's style template file selects the citation order to be ``citenum`` or ``none``, then creating the ordered citation list is as simple as listing the citation keys in order of their citation appearance, which was recorded as the value in the citation dictionary. If the user instead chooses the citation order to be ``citekey``, then all that is needed is to sort the citation keys alphabetically. Similar operations follow for the various citation order options, but the difficult lies in correctly sorting in the presence of non-ASCII languages, and especially in the presence of LaTeX markup of non-ASCII names. For a citation sorting order that requires using author names, any LaTeX markup needs to be converted to its Unicode equivalent prior to sorting. Using unicode allows the sorting to be done with any input languages, and allows the sorting order to be locale-dependent.

``create_citation_list()`` is the highest-level function for generating the citation list. For each citation key, it calls ``generate_sortkey()``, which is the workhorse function for including all of the various options when generating the key to use for sorting the list. A key part of the function is a call to ``purify_string()``, which removes unnecessary LaTeX markup elements and then calls ``latex_to_utf8()`` to convert LaTeX-markup non-ASCII characters to Unicode. It is only after all of these conversions that the final sorting is performed and the sorted citation list returned.

Testing
=======

The suite of regression tests for Bibulous consist of various template definitions and database entries designed to test individual features of the program. The basic approach of the tests is as follows:

    1. Once a change is made to the code (to fix a bug or add functionality), the developer also adds an entry to the ``test/test1.bib`` file, where the entry's "entrytype" is named in such a way to give an indication of what the test is for. For example, the entry in the BIB file may be defined with::

           @test_initialize1{...

       where the developer provides an ``author`` field in the entry where one or more authors have names which are difficult to for generating initials correctly. The developer should also include at least a 1-line comment about the purpose of the entry as well. To make everything easy to find, use the entrytype as the entry's key as well. Thus, the example above would use::

           @test_initialize1{test_initialize1, ...

    2. If the above new entry is something which can be checked with normal options settings, then the developer should add a corresponding line in the BST file defining how that new entrytype (i.e. ``test_initialize1``) should be formatted. If *different* options settings are needed, then a new BST file is needed. Only a minimalist file is generally needed: the file can, for example, contain one line defining a new entrytype and one line to define the new option setting. You can define all of the other options if you want, but these are redundant and introduce a number of unnecessary "overwriting option value..." warning messages.
    3. Next, the developer should add a line ``\citation{entrytype}`` to the AUX file where the key is the key given in the new entry of the BIB file you just put in (e.g. ``test_initialize1``). This is the same as the entrytype to keep everything consistent.
    4. Next, the developer needs to add two lines to the ``test1_target.bbl`` file to say what the formatted result should look like. Take a look at other lines to get a feel for how these should look, and take in consideration the form of the template just added to the BST file.
    5. Finally, run ``bibulous_test.py`` to check the result. This script will load the modified BIB and BST files and will write out several formatted BBL file ``test1.bbl`` etc. It will then run a ``diff`` program on the output file versus the target BBL file to see if there are any differences between the target and actual output BBL files.

Generating the documentation
============================

From the bibulous repository ``doc/`` subfolder, run ``make html`` to generate the HTML documentation. The result can be found in ``doc/_build/html/``, with ``index.html`` as the main file. To generate the PDF documentation, run ``make latexpdf`` from the ``doc/`` subfolder, with the result found at ``doc/_build/latex/Bibulous.pdf``.
