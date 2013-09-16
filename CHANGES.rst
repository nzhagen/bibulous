version 1.0 (02-Jun-2013)
------------------------

- Initial release.


version 1.1 (19-Aug-2013)
------------------------

- Changed the program flow to use database extraction by default. This can provide dramatic
  speedups for the use case of calling a large database using a small number of citations,
  when there are no new citations added to the auxiliary file.


version 1.2 (11-Sep-2013)
-------------------------

- Moved the way that citation labels and sortkeys are generated from using keywords to using
  templates.
- Added the ability to use nested options brackets, as in [[<var1>|<var2>]|<var3>|].


