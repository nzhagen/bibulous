Installing Bibulous
===================

[add some notes here]

Kile: replacing BibTeX with Bibulous
------------------------------------

1. In your *.tex file, change the filename of the \bibliography{...} command to the filename for the appropriate Bibulous-format bibliography style template (*.bst file).

2. In Kile, go to the menu bar and select ``Settings`` > ``Configure Kile``. Select ``Tools`` > ``Build`` and choose ``BibTeX`` from the ``Select a tool`` menu (see the figure). To the right of the menu, after you select ``BibTeX`` you should see "Choose a configuration for the tool BibTeX". Below the drop-down menu, select the button "New" and type in the name ``Bibulous`` (or whatever you prefer to call your new tool). Below, in the ``General`` tab, type in the location of the ``bibulous.py`` file. And in the ``Options`` field, type::

    \begin{Verbatim}
    '%S.tex'
    '%source'
    \end{Verbatim}

That should be it. In case your default setup is different, you can also check the ``Advanced`` tab settings and verify that they are as shown in the second figure. (That is, ``Source extension`` is set to ``aux``, and ``Target extension`` is set to ``bbl``.)

Modifying WinEdt5 to replace BibTeX with Bibulous
-------------------------------------------------

1. Go to the menu ``Options`` > ``Execution Modes``. In the ``Console Applications`` menu on the left hand side, select ``BibTeX``. Then replace the three ``Command Line`` fields with the ones shown in the figure, replacing the files paths with the ones correct for your installation of Python and ``bibulous.py``.

2. Note that the following are definitions of WinEdt registers::

   %f = full path of active file (= %p/%n.%t)
   %n = name of the active file
   %p = the path of the active file
   %t = the extension of the active file
   %q = the path relative to the main file (i.e. for subdirectories)
   %b = WinEdt's local working directory (not the tex file directory)
   %B = path to the WinEdt executable file
