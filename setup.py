#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = "bibulous",
    py_modules = ['bibulous', 'bibulous_test', 'bibulous_authorextract'],
    package_dir = {'':'.'},
    packages = find_packages(exclude=['test']),
    version = "2.0",
    description = "BibTeX replacement and enhancement",
    author = "Nathan Hagen",
    author_email = "and.the.light.shattered@gmail.com",
    url = "https://github.com/nzhagen/bibulous",
    download_url = "https://github.com/nzhagen/bibulous/blob/master/bibulous.py",
    license = "MIT",
    keywords = ["bibtex", "bibliography", "parser", "tex", "latex"],
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Text Processing",
        ],
    long_description = """\
A drop-in replacement for BibTeX based on string templates.
-----------------------------------------------------------

Bibulous provides a flexible way of accomplishing the same tasks as BibTeX, and going
beyond it in capability. Some of its advantages include:

  - An integrated BibTeX database file (.bib file) parser.
  - Fully internationalized: Bibulous can use bibliography databases and bibliography style
    files written in any language.
  - Simple and powerful customization: style templates are an ideal way of visualizing and
    manipulating bibliography styles. There is no need to learn BibTeX's arcane stack-based
    language in order to build or customize a bibliography style.
  - Multilingual capability: templates are largely language agnostic, so that multilingual
    bibliographies can be achieved almost effortlessly.
  - Users can build glossaries, lists of symbols, and lists of acronyms using the same
    infrastructure as used for bibliographies.
  - Sorting of citations is fully localized and has no difficulty in dealing with strings
    that contain Unicode, LaTeX-markup characters for non-English languages, or even
    mathematics markup.

This version requires Python 3.6 or later.
"""
)
