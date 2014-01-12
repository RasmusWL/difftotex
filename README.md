difftotex
=========

Useful when teachers require that you *"include in the report the most important code that you yourself wrote or modified."*

For each file it creates a heading *(like section/subsection -- is customizeable)* and a label with the filename *(also customizeable)*

Requirements
============

* Python 3.2+
* a TeX enviroment

Usage
=====

    $ git diff --no-color > somefile.diff
    $ SOMEPATH/difftotex.py somefile.diff

or

    $ git diff --no-color | SOMEPATH/difftotex.py

This will create the file `diff.tex` in your current directory.

[**Help me create a diff!**](#faq-for-generating-diffs)

========================

To change the path of output file, use the `-o` options, like so

    $ SOMEPATH/difftotex.py -o path/output.tex somefile.diff

*- adding options to the end is also accepted*

========================

To learn about the "advanced" options run `SOMEPATH/difftotex.py --help` *(like changing the section level to "subsubsection")*

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

Here is a small example for a libgit2 [commit](https://github.com/libgit2/libgit2/commit/08283cbdb857d09f8e623c5c23abcaa499b6b3fc) -- below is a preview of the [pdf](/example/parent.pdf)

![examplepng](https://raw2.github.com/RasmusWriedtLarsen/difftotex/master/example/example.png)

Known Limitations
=================
* Can only parse git diffs (not other formats)
* Will completely ignore binary files listed in the diff
* Tab size is fixed to 4 spaces
* TeX code gets really ugly (special characters are escaped manually, due to the fact that I couldn't find a combination of multipage tables working with an in-cell verbatim enviroment)

FAQ for generating diffs
========================
#### Basics
You need to specify a reference to the commit you want to base your diff on, lets call it `<start-commit>`. To generate the diff up till the current commit, simply run `git diff --no-color start-commit` -- you can also specify a commit to end at, as `git diff --no-color start-commit end-commit`

#### How do I find a reference to the initial commit?
run `git rev-list --max-parents=0 HEAD` to list all root commits (there can be more than one)

#### Only include some subfolders
If you want to restrict paths included, e.g. only include folders `src` and `data`, run `git diff --no-color start-commit end-commit -- src data`

#### Don't use full path from project root.
When you want `<git-project>/src/file.c` listed as `file.c`, cd to `<git-project>/src/` and add the `--relative` option. (will restrict diff to current folder and subfolders)

#### For changes I have made, include the *whole* file
Add the option `-U10000000` (will include the nearst 10,000,000 lines of code)

#### For changes I have made, include the *whole* function
Add the option `-W`



