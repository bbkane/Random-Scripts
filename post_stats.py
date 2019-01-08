#!/usr/bin/env python3

from collections import Counter
from pathlib import Path
import string
import sys

# This script goes through my _posts directory, strips
# out lines surrounded by ``` or --- blocks, then does a little
# statistics on the results


def is_valid_word(word):
    contains_letters = any(c in string.ascii_letters for c in word)
    not_a_variable = '`' not in word
    return contains_letters and not_a_variable


def munge_word(word):
    """ return the lowercase word with trailing/preceding punctuation stripped"""
    word = word.lower()
    if word and word[-1] not in string.ascii_lowercase:
        word = word[:-1]
    if word and word[0] not in string.ascii_lowercase:
        word = word[1:]
    return word


def main():

    counter = Counter()
    word_count = 0

    topdir = sys.argv[1]

    for path in Path(topdir).glob('*.md'):
        with open(path) as blog_post:
            is_code = False
            for line in blog_post:
                if line.startswith('```') or line.startswith('---'):
                    is_code = not is_code
                    continue
                if not is_code:
                    # print(line, end='\n')

                    # now get stats :)
                    for word in line.split():
                        word = word.strip()
                        if is_valid_word(word):
                            word_count += 1
                            munged_word = munge_word(word)
                            counter[munged_word] += 1

    print()
    print('Word Count: ', word_count)
    print()

    # print(counter.most_common(100))
    print("| order | word | count |")
    print("|=======|======|=======|")
    for order, mci in enumerate(counter.most_common(50)):
        word, count = mci
        print(f"| {order + 1} | {word} | {count} |")


if __name__ == "__main__":
    main()
