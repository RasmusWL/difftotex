#!/usr/bin/env python3

import tex, diffparser, argumentparser
from classes import *

def main():
    (inputLines) = argumentparser.parse_cli()

    files = diffparser.parseLines( inputLines, settings.diffPrefixRegex )

    tex.output(files)

if __name__ == "__main__":
   main()
