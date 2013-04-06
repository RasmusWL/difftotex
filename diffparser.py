import re
from classes import *

def parseDiffLine(line):
    diffLine = DiffLine()

    if line.startswith("-"):
        diffLine.state = DiffLineState.DELETE
    elif line.startswith("+"):
        diffLine.state = DiffLineState.INSERT
    elif line.startswith(" "):
        diffLine.state = DiffLineState.UNCHANGED
    else:
        return None

    diffLine.text = line
    return diffLine

def transformFilename(filename, regex):
    return ( re.sub(regex, "", filename) )

def parseLines(lines, diffPrefixRegex):
    diffFiles = []
    diffFile = None
    change = None

    for line in lines:

        if line.startswith("diff"):
            diffFile = DiffFile()
            diffFiles.append(diffFile)

        elif line.startswith("@@"):
            oldStartLine = int( line[ line.find("-")+1:line.find(",")] )
            newStartLine = int( line[ line.find("+")+1:line.find(",", line.find("+"))] )

            change = DiffChange()
            diffFile.changes.append(change)

            change.oldStartLine = oldStartLine
            change.newStartLine = newStartLine
            change.description = line

        elif line.startswith("---"):
            diffFile.oldPath = transformFilename(line[4:], diffPrefixRegex)

        elif line.startswith("+++"):
            diffFile.newPath = transformFilename(line[4:], diffPrefixRegex)

            diffFile.pathChanged = diffFile.newPath != diffFile.oldPath

        else:
            diffLine = parseDiffLine(line)
            if ( diffLine is None):
                continue
            change.lines.append( diffLine )

    return diffFiles