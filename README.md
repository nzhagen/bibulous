bibulous
========

Bibulous - a simple drop-in replacement for BibTeX using style templates.

Bibulous developed out of frustrations with developing bibliography styles using BibTeX's obscure style file language, and from the realization that bibliographies are highly structured, so that they can be specified simply and flexibly using a template approach. With templates, one can develop entirely new bibliography styles in a matter of minutes, and often without having to refer to the user manual during the entire process.

At the same time, an attempt has been made to incorporate a lot of the modern enhancements to BibTeX, such as the ability to work with languages other than English, allowing use of non-standard bibliography entry types, functionality for enhanced citation styles, etc. It also eliminates the attachment to some of BibTeX's quirks, such as its reduction of uppercase letters in titles (which is left as an option), and its sometimes awkward name formatting, among others.

Other packages have implied that BibTeX's dependence on .bst files is a drawback to its operation, but Bibulous takes the opposite approach and treats it as an advantage: the BibTeX style file (now termed a "bibliography style template") allows a user to visualize the entire bibliography format structure in a concise and easy to read single page of text. The grammatical structure of the template is sufficiently powerful to allow users to develop other tools based on the same code base: glossaries, lists of nomenclatures, etc.
