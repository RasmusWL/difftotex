import re
from classes import *

getLinesNumsRE = re.compile(r'@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@')

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

def hackRemoveNonValid(diffFiles):
    # Iterate backwards, as forward iteration does not handle removing items
    for diffFile in reversed(diffFiles):
        #diffFile = diffFiles[i]
        if diffFile.changes == []:
            if not settings.quiet:
                print ( "Removing invalid input: %s" % (diffFile.diffLine) )
            diffFiles.remove(diffFile)

def parseLines(lines, diffPrefixRegex):
    diffFiles = []
    diffFile = None
    change = None

    lineNum = 0

    try:
        for line in lines:
            lineNum += 1

            if line.startswith("diff"):
                diffFile = DiffFile()
                diffFiles.append(diffFile)
                diffFile.diffLine += line

            elif line.startswith("@@"):
                (oldStr, newStr) = getLinesNumsRE.match(line).groups()

                change = DiffChange()
                diffFile.changes.append(change)

                change.oldStartLine = int(oldStr)
                change.newStartLine = int(newStr)
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
    except Exception as e:
        raise ParseError(lineNum, e)


    hackRemoveNonValid(diffFiles);

    return diffFiles
