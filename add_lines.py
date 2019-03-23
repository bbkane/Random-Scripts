#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
from textwrap import dedent
import argparse
import re
import statistics
import sys
import typing

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
This script parses a text file to gather simple stats on lines. It's useful
for interspersing budget itmes in notes.

Count lines like: <marker> <category> <name> <amount>  # optional comment
By default <marker> is ;;

Example line:
    ;; Budget BankAccount 9999999999  # got dat money


Examples BASH usage:
    {sys.argv[0]} text.txt

    {sys.argv[0]} < text.txt

    cat <<EOF | {sys.argv[0]}
    ;; Points Ben 1
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
        f"^{marker}" + r"""
        \s+
        (?P<category>\w+)
        \s+
        (?P<name>\w+)
        \s+
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


def test_match_lines(marker):
    """Poor man's in-file pytest"""
    lines = dedent("""
    ;; CA   A 1
    ;; CB B 1.1
    ;; CC C 1
    ;; CD D  1
    ;; CE E   1
    ;; CF F -1
    ;; Ct t     10 # bob
    """).strip()

    for i, line in enumerate(lines.split('\n')):
        line += '\n'
        print(f'{i}: Testing: {repr(line)}')
        match = match_line(line, marker)
        print(f'{i}: Match: {repr(match)}')
        item = Item.from_regex_match(match, i)
        print(f'{i}: Result: {repr(item)}')
        print()


class Item(typing.NamedTuple):
    line_number: int
    category: str
    name: str
    amount: float
    comment: typing.Optional[str]

    @classmethod
    def from_regex_match(cls, match, line_number):
        i = cls(
            line_number=line_number,
            category=match['category'],
            name=match['name'],
            amount=float(match['amount']),
            comment=match['comment'],
        )
        return i


def main():
    args = parse_args()

    if args.testing:
        test_match_lines(args.marker)
        return

    items = []
    for i, line in enumerate(args.infile):
        match = match_line(line, args.marker)
        if match:
            items.append(Item.from_regex_match(match, i))

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
