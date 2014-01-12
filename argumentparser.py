import argparse
import os, sys

from classes import *
from difftotex import version

description = """\
Create latex from git diff supplied in FILE or standard input.
Make sure it does not contain coloring: add option --no-color to git diff cmd
"""

epilog = """\
Make sure to include the following in your preamble:
\\usepackage{array}
\\usepackage{tabu}
\\usepackage{longtable}
\\usepackage[table]{xcolor}
"""

defaultFilename = "diff.tex"
defaultSection = "sub"

defaultDiffPrefixRegex = "^(a|b)/"

mapping = {
"part":"part",
"sec":"section",
"sub":"subsection",
"subsub":"subsubsection",
"par":"paragraph"
}

sectionChoices = ["part", "sec", "sub", "subsub", "par"]

parser = argparse.ArgumentParser(usage='%(prog)s [OPTION ...] [FILE]', description=description, epilog=epilog,
                                formatter_class=argparse.RawDescriptionHelpFormatter,)

parser.add_argument(dest='infile', metavar="FILE", nargs="?",
                    help='input diff file, if none specified, uses standard input')

parser.add_argument('--version', action='version',
                    version='%(prog)s version {}'.format(version) )

parser.add_argument('-o', dest='outfile', metavar="FILE", default = defaultFilename,
                    help='place the output into FILE (default: {})'.format(defaultFilename) )

group = parser.add_mutually_exclusive_group()

group.add_argument('--section', dest='section', default = defaultSection,
                    choices=sectionChoices,
                    help='''section level for file title -- will also set label prefix
                    -- (default: {})'''.format(defaultSection) )

group.add_argument('--custom-section', dest='customsection', metavar="STR",
                    help='custom section level for file title' )

parser.add_argument('--custom-label', dest='customlabel', metavar="STR",
                    help='custom label prefix for file title' )

parser.add_argument('--no-label', dest='nolabel', action="store_const",
                    const=True, default=False,
                    help="don't create labels for file title")

parser.add_argument('--diff-path-regex', dest='diffPrefixRegex', metavar="RE",
                    default = defaultDiffPrefixRegex,
                    help="""Regular expression, used to remove parts of the file paths.
                    git diff will by default prefix old with "a/" and
                    new with "b/". (default: {})""".format(defaultDiffPrefixRegex) )

parser.add_argument('-q', '--quiet', dest='quiet', action="store_const",
                    const=True, default=False,
                    help="don't print messages")

def parse_cli():
    args = parser.parse_args()

    if args.outfile is None:
        settings.outfile = "diff.tex"
    else:
        dirname = os.path.dirname(args.outfile)
        if dirname != "" and not os.path.isdir( dirname ):
            print("output file is not in an existing folder")
            sys.exit(2)

        settings.outfile = args.outfile

    if args.customsection:
        settings.headingStyle = args.customsection
    else:
        settings.labelPrefix = args.section + ":"
        settings.headingStyle = mapping[args.section]

    if args.customlabel:
        settings.labelPrefix = args.customlabel + ":"
    elif args.customsection and not args.nolabel:
        print("Custom section level, but no custom label prefix, prefix will not be used")
        settings.labelPrefix = ""

    settings.shouldAddLabel = not args.nolabel

    settings.diffPrefixRegex = args.diffPrefixRegex

    inputLines = None;
    if args.infile:
        if not os.path.isfile(args.infile):
            print("%s did not exist" % args.infile)
            exit(2)
        f = open(args.infile)
        inputLines = f.read().splitlines()
        f.close()
    else:
        inputLines = sys.stdin.read().splitlines()

    settings.quiet = args.quiet

    return (inputLines)
