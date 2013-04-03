difftotex
=========

Useful when teachers require that you *"include in the report the most important code that you yourself wrote or modified."*

For each file it creates a heading *(like section/subsection -- is customizeable)* and a label with the filename *(also customizeable)*

Requirements
============

* Python 3.2
* a TeX enviroment

Usage
=====

    $ git diff --no-color > somefile.diff
    $ SOMEPATH/difftotex.py somefile.diff

or

    $ git diff --no-color | SOMEPATH/difftotex.py

To learn about the "advanced" options run `SOMEPATH/difftotex.py --help` *(like changing the output file)*

Remember to remove color codes from the diff

Latex
-----

Include the following in your preabmle

```tex
\usepackage{array}
\usepackage{tabu}
\usepackage{longtable}
\usepackage[table]{xcolor}
```

and then input the diff

    \input{diff.tex}

Example
=======

Here is a small example for a libgit2 [commit](https://github.com/libgit2/libgit2/commit/08283cbdb857d09f8e623c5c23abcaa499b6b3fc) see below for a preview of the [pdf](/example/parent.pdf)

![examplepng](/example/example.png)

Known Limitations
=================
* Can only parse git diffs (not other formats)
* Only works for plain text files (quick fix is to manually remove other files from diff)
* Won't catch any errors
* Tab size is fixed to 4 spaces
* TeX code gets really ugly (special characters are escaped manually, due to the fact that I couldn't find a combination of multipage tables working with an in-cell verbatim enviroment)
