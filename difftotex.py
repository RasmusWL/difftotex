#!/usr/bin/python3.2

import tex, diffparser, argumentparser
from classes import *

def main():
    (inputLines, settings) = argumentparser.parse_cli()

    files = diffparser.parseLines( inputLines, settings.diffPrefixRegex )

    tex.output(files, settings)

if __name__ == "__main__":
   main()
