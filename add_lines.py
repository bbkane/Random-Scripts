#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
from textwrap import dedent
import argparse
import re
import statistics
import sys

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
This script parses a text file to gather simple stats on lines. It's useful
for interspersing budget itmes in notes.

Count lines like: <marker> <name> <separator> <amount>  # optional comment
By default <marker> is ;; and <separator> is ,

Example line:
    ;; BankAccount , 9999999999  # got dat money


Examples BASH usage:
    {sys.argv[0]} text.txt

    {sys.argv[0]} < text.txt

    cat <<EOF | {sys.argv[0]}
    ;; Ben , 1
    EOF

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
        '--separator',
        '-s',
        default=',',
        help='Separator between name and amount. Defaults to ,'
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


def match_line(line, marker, sep):
    pattern = re.compile(
        f"^{marker}" + r"""\s+
        (?P<name>\w+)
        \s*
        """ + re.escape(sep) + r"""
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


def test_match_lines(marker, separator):
    """Poor man's in-file pytest"""
    lines = dedent("""
    ;; A , 1
    ;; B , 1.1
    ;; C,1
    ;; D, 1
    ;; E ,1
    ;; F ,-1
    ;; t , 10 # bob
    """).strip()

    for i, line in enumerate(lines.split('\n')):
        line += '\n'
        print(f'{i}: Testing: {repr(line)}')
        d = match_line(line, marker, separator)
        print(f'{i}: Result: {repr(d)}')
        print()


def main():
    args = parse_args()

    if args.testing:
        test_match_lines(args.marker, args.separator)
        return

    items = []
    for i, line in enumerate(args.infile):
        d = match_line(line, args.marker, args.separator)
        if d:
            if args.verbose:
                print(f'line: {i}: {d}')
            d['amount'] = float(d['amount'])
            items.append(d)

    if items:
        print(f'Num Items: {len(items)}')

        total = sum(i['amount'] for i in items)
        print(f'Sum:  {total}')

        mean = statistics.mean(i['amount'] for i in items)
        print(f'Mean: {mean}')

        minimum = min(items, key=itemgetter('amount'))
        print(f'Min:  {minimum}')

        maximum = max(items, key=itemgetter('amount'))
        print(f'Max:  {maximum}')
    else:
        print(f'No number lines found')


if __name__ == "__main__":
    main()
