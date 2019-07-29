Frequently asked questions
**************************

1. What is the difference between using Bibulous and using BibLatex+Biber?
==========================================================================

The biggest difference between these two is that Bibulous uses bibliography style template files that are intuitive and compact, whereas the Bibulous+Biber combination uses LaTeX code to generate styles, and these make them much more difficult to create and customize. A question posted on StackExchange [http://tex.stackexchange.com/questions/151628/bibtex-fields-for-doi-mr-zbl-and-arxiv/163628#163628] asked how one can build a reference list with hyperlinks to zbl, mr, doi, and eprint fields as defined in the database entries.

For Bibulous, we can create a template file, or modify an existing one, to have a ``link`` variable (you can call it almost anything you like), and add a definition for ``link`` in the ``SPECIAL-TEMPLATES`` section of the file::

    TEMPLATES:
    arxiv = <au>. <title>. <year>. arXiv: \href{http://arxiv.org/abs/<eprint>}{<eprint>}.
    article = <au>. <title>. <journal>, <volume>[(<number>)]:[<startpage>--<endpage>|<startpage>|<eid>|], <year>.[<link>]
    SPECIAL-TEMPLATES:
    link = [ doi: \href{http://dx.doi.org/<doi>}{<doi>}.][ MR: \href{http://www.ams.org/mathscinet-getitem?mr=MR<mr>}{<mr>}.][ Zbl: \href{http://zbmath.org/?q=an:<zbl>}{<zbl>}.]

The definition for ``link`` in the ``SPECIAL-TEMPLATES`` section creates a variable that can be used in the entrytype style templates. Thus, any template can use ``<link>`` to insert a hyperref to the quantities defined in the database. Adding the definition, and inserting ``<link>`` in each template where desired is all that needs to be done. The square brackets around ``<link>`` tell the template to ignore it if none of the four fields is defined inside the database entry.

For BibLatex+Biber, we can compare to Bibulous by using the answer provided on the same StackExchange page, given as follows. We add the following lines to the preamble of the main ``tex`` file::

    \DeclareDatamodelFields[type=field,datatype=verbatim]{arxiv,mr,zbl,jstor,hdl,pubmed,googlebooks,pmcid}
    \DeclareDatamodelEntryfields{arxiv,mr,zbl,jstor,hdl,pubmed,googlebooks,pmcid}
    \DeclareDatamodelFields[type=field,datatype=literal]{arxivclass}
    \DeclareDatamodelEntryfields{arxivclass}
    \DeclareSourcemap{
    \maps[datatype=bibtex]{
        \map{
        \step[fieldsource=pmid, fieldtarget=pubmed]
        }
    }
    }
    \makeatletter
    \DeclareFieldFormat{arxiv}{%
    arXiv\addcolon\space
    \ifhyperref
        {\href{http://arxiv.org/\abx@arxivpath/#1}{%
        \nolinkurl{#1}%
        \iffieldundef{arxivclass}
            {}
            {\addspace\texttt{\mkbibbrackets{\thefield{arxivclass}}}}}}
        {\nolinkurl{#1}
        \iffieldundef{arxivclass}
        {}
        {\addspace\texttt{\mkbibbrackets{\thefield{arxivclass}}}}}}
    \makeatother
    \DeclareFieldFormat{pmcid}{%
    PMCID\addcolon\space
    \ifhyperref
        {\href{http://www.ncbi.nlm.nih.gov/pmc/articles/#1}{\nolinkurl{#1}}}
        {\nolinkurl{#1}}}
    \DeclareFieldFormat{mr}{%
    MR\addcolon\space
    \ifhyperref
        {\href{http://www.ams.org/mathscinet-getitem?mr=MR#1}{\nolinkurl{#1}}}
        {\nolinkurl{#1}}}
    \DeclareFieldFormat{zbl}{%
    Zbl\addcolon\space
    \ifhyperref
        {\href{http://zbmath.org/?q=an:#1}{\nolinkurl{#1}}}
        {\nolinkurl{#1}}}
    \DeclareFieldAlias{jstor}{eprint:jstor}
    \DeclareFieldAlias{hdl}{eprint:hdl}
    \DeclareFieldAlias{pubmed}{eprint:pubmed}
    \DeclareFieldAlias{googlebooks}{eprint:googlebooks}
    \renewbibmacro*{eprint}{%
    \printfield{arxiv}%
    \newunit\newblock
    \printfield{jstor}%
    \newunit\newblock
    \printfield{mr}%
    \newunit\newblock
    \printfield{zbl}%
    \newunit\newblock
    \printfield{hdl}%
    \newunit\newblock
    \printfield{pubmed}%
    \newunit\newblock
    \printfield{pmcid}%
    \newunit\newblock
    \printfield{googlebooks}%
    \newunit\newblock
    \iffieldundef{eprinttype}
        {\printfield{eprint}}
        {\printfield[eprint:\strfield{eprinttype}]{eprint}}}

The template approach is clearly more compact, easier to read, and easier to customize.
