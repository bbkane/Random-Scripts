#!/usr/bin/env python
# -*- coding: utf-8 -*-

from textwrap import dedent
import argparse
import re
import statistics
import sys

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
Count lines like: <marker> <name> , <amount>  # optional comment
By default <marker> is ;;

The intent for this script is to be able to calculate simple stats on notes by
including lines like the above interspersed in text files

Examples:
    {sys.argv[0]} text.txt
    {sys.argv[0]} < text.txt

Help:
Please see Benjamin Kane for help.
Code at https://github.com/bbkane/Random-Scripts/tree/master
"""


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Use a file or stdin for an argument
    # https://stackoverflow.com/a/11038508/2958070
    parser.add_argument(
        'infile',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='Use a file or stdin'
    )

    parser.add_argument(
        '--marker',
        '-m',
        default=';;',
        help='Marker at front of line to mark line to count. Defaults to ;;'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Print numeric lines as found'
    )
    parser.add_argument(
        '--testing',
        '-t',
        action='store_true',
        help='Run some quick tests'
    )

    return parser.parse_args(*args, **kwargs)


def match_line(line, marker):
    pattern = re.compile(
        f"^{marker}" + r"""\s+
        (?P<name>\w+)
        \s*
        ,
        \s*
        (?P<amount>
            [+-]?             # optional signe
            [0-9]+            # some digits
            (\.[0-9]*)?       # optional decimal part
        )
        \s*                   # can end in whitespace
        (
            \#\s*
            (?P<comment>.*)
        )?                    # or end in optional comment starting with hash
        \n""",
        re.VERBOSE
    )
    match = re.match(pattern, line)
    if match:
        return match.groupdict()
    return None


def test_match_lines():
    """Poor man's in-file pytest"""
    lines = dedent("""
    ;; A , 1
    ;; B , 1.1
    ;; C,1
    ;; D, 1
    ;; E ,1
    ;; F ,-1
    """).strip()

    for line in lines.split('\n'):
        line += '\n'
        print(f'Testing: {repr(line)}')
        d = match_line(line, ';;')
        print(f'Result: {repr(d)}')
        print()


def main():
    args = parse_args()
    if args.testing:
        test_match_lines()
        return
    numbers = []
    for line in args.infile:
        d = match_line(line, args.marker)
        if d:
            if args.verbose:
                print(d)
            numbers.append(float(d['amount']))
    print(f'Sum:  {sum(numbers)}')
    print(f'Mean: {statistics.mean(numbers)}')
    print(f'Min:  {min(numbers)}')
    print(f'Max:  {max(numbers)}')


if __name__ == "__main__":
    main()
