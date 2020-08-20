#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import dataclasses
import sys
import typing as ty

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
<description>
Examples:
    {sys.argv[0]}
Help:
Please see Benjamin Kane for help.
Code at <repo>
"""


@dataclasses.dataclass
class TaxBracket:
    income_start: float
    income_end: float
    tax_unit_interval: float


def tax(income: float, tax_brackets: ty.List[TaxBracket]) -> float:
    total_tax = 0.0
    for bracket in tax_brackets:
        if income > bracket.income_start:
            to_tax = min(income, bracket.income_end) - bracket.income_start
            tax = to_tax * bracket.tax_unit_interval
            total_tax += tax
    return total_tax


def main():

    tax_brackets = [
        TaxBracket(income_start=0, income_end=9_875, tax_unit_interval=0.1),
        TaxBracket(income_start=9_875, income_end=40_125, tax_unit_interval=0.12),
        TaxBracket(income_start=40_126, income_end=85_525, tax_unit_interval=0.22),
        TaxBracket(income_start=85_526, income_end=163_300, tax_unit_interval=0.24),
        TaxBracket(income_start=163_301, income_end=207_350, tax_unit_interval=0.32),
        TaxBracket(income_start=207_351, income_end=518_400, tax_unit_interval=0.35),
        TaxBracket(income_start=518_401, income_end=float('inf'), tax_unit_interval=0.37),
    ]

    for i in range(1, 1_000_000, 5000):
        print(f"{i}\t{tax(i, tax_brackets)/i}")


if __name__ == "__main__":
    main()

