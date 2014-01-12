#!/usr/bin/env python3

import tex, diffparser, argumentparser
from classes import *

version = "0.1.1"
debug = False

def main():
    (inputLines) = argumentparser.parse_cli()

    files = diffparser.parseLines( inputLines, settings.diffPrefixRegex )

    try:
        tex.output(files)
    except Exception as e:
        raise ToTexError(e)

if __name__ == "__main__":
    realException = None
    try:
        main()
    except (ParseError, ToTexError) as e:
        print ("")
        print (str(e))
        print ("")
        print ("If you think this is not your fault, please submit an issue,")
        print ("preferably including your diff file, at")
        print ("https://github.com/RasmusWriedtLarsen/difftotex")
        realException = e.e
    except KeyboardInterrupt:
        print (" Thank you, come again!")

    if debug and realException != None:
        print ("\n")
        raise realException
