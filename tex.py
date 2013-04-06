from classes import *

latexBegin = r'''
% +-----------------------------------------------------+
% |   You must include the following in your preamble   |
% +-----------------------------------------------------+
% \usepackage{array}
% \usepackage{tabu}
% \usepackage{longtable}
% \usepackage[table]{xcolor}
% +-----------------------------------------------------+
% |                         end                         |
% +-----------------------------------------------------+

\definecolor{DiffInsertRGB}{RGB}{221,255,221}
\definecolor{DiffDeleteRGB}{RGB}{255,221,221}
\definecolor{DiffLineNumber}{RGB}{170,170,170}
'''

latexFileHeading = "\\%s{%s\label{%s%s}}"
latexFileHeadingNoLabel = "\\%s{%s}"

latexTableBegin = r'''
{\ttfamily\scriptsize

\begin{longtabu} to \linewidth {|>{\color{DiffLineNumber}}r|>{\color{DiffLineNumber}}r|X|}

\hline
'''

latexTableEnd = r'''
\hline
\end{longtabu}
}
'''

latexLineInsert = '& %d & \\cellcolor{DiffInsertRGB} %s \\tabularnewline'
latexLineDelete = '%d & & \\cellcolor{DiffDeleteRGB} %s \\tabularnewline'
latexLineUnchanged = '%d & %d & %s \\tabularnewline'
latexDescrition = '... & ... & \\textcolor{DiffLineNumber}{%s} \\tabularnewline'

latexReplacements = {
    '\t': '\\ ' * 4,
    '&': '\\&',
    '%': '\\%',
    '$': '\\$',
    '#': '\\#',
    '_': '\\_',
    '{': '\\{',
    '}': '\\}',
    '~': '\\textasciitilde ',
    '^': '\\textasciicircum '
}

def escapeForLatex(text):
    text = text.replace('\\', '\\textbackslash')
    text = text.replace(' ', '\\ ')
    text = text.replace('\\textbackslash', '\\textbackslash ')

    for i, j in latexReplacements.items():
        text = text.replace(i, j)

    text = text.replace('"', '\char`\"{}')
    return text

def output(files, settings):
    outlines = []

    outlines.append(latexBegin)

    for fil in files:
        fileName = fil.newPath

        if fil.pathChanged:
            if fil.newPath == "/dev/null":
                fileName = fil.oldPath
            elif fil.oldPath != "/dev/null":
                fileName = "".join( [fil.oldPath, " => ", fil.newPath] )

        if settings.shouldAddLabel:
            # apparently, no escape in labels
            heading = latexFileHeading % (settings.headingStyle, escapeForLatex(fileName), settings.labelPrefix, fileName)
        else:
            heading = latexFileHeadingNoLabel % (settings.headingStyle, escapeForLatex(fileName) )

        outlines.append(heading)


        outlines.append(latexTableBegin)

        for change in fil.changes:
            oldLine = change.oldStartLine
            newLine = change.newStartLine

            outlines.append( latexDescrition % ( escapeForLatex(change.description) ) )

            for line in change.lines:
                if line.state == DiffLineState.INSERT:
                    outlines.append( latexLineInsert % (newLine, escapeForLatex(line.text) ) )

                    newLine += 1
                elif line.state == DiffLineState.DELETE:
                    outlines.append( latexLineDelete % (oldLine, escapeForLatex(line.text) ) )

                    oldLine += 1
                elif line.state == DiffLineState.UNCHANGED:
                    outlines.append( latexLineUnchanged % (oldLine, newLine, escapeForLatex(line.text) ) )

                    oldLine += 1
                    newLine += 1

        outlines.append(latexTableEnd)


    f = open(settings.outfile, "w")
    f.write("\n".join(outlines))
    f.close()
