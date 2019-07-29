version 1.0 (02-Jun-2013)
------------------------

- Initial release.


version 1.1 (19-Aug-2013)
------------------------

- Changed the program flow to use database extraction by default. This can provide dramatic
  speedups for the use case of calling a large database using a small number of citations,
  when there are no new citations added to the auxiliary file.


version 1.2 (24-Sep-2013)
-------------------------

- Moved the way that citation labels and sortkeys are generated from using keywords to using
  templates.
- Added the ability to use nested options brackets, as in [[<var1>|<var2>]|<var3>|].
- Added the ability to use indexes to sequence-type variables (such as <name.0.last> within templates.
- Also added the ability to use function mapping on variables (such as <name.initial()>).


version 1.3 (08-Nov-2013)
-------------------------

- Added template variable operators.
- Added implicit looping inside template strings using ellipsis notation with indexed variables.
- Added implicit indexing with ".n" notation for template variables.
- Changed the code from using internal structures to formatting name lists to using namelist
  templates instead. This allows users to easily customize how lists of names are formatted.
- Added an "Examples" section to the documentation.

version 2.0 (29-Jul-2019)
-------------------------

- Upgraded the code to Python3 compatibility.
- Add a number of small bug fixes, typo corrections, and template tweaks.
