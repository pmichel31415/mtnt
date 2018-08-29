#!/usr/bin/env python
"""Counts the ratio between UK and US version of words

Looks at ise/ize
"""

import re

# Detects -ise/-ize words
ise_regex = re.compile(r'\w+is(e|ation|ing)s?$', re.I)
ize_regex = re.compile(r'\w+iz(e|ation|ing)s?$', re.I)

N_UK = N_US = 0
try:
    while True:
        line = input()
        for w in line.strip().split():
            if ise_regex.search(w):
                N_UK += 1
            elif ize_regex.search(w):
                N_US += 1
except (KeyboardInterrupt, EOFError):
    pass
finally:
    print('%%UK\t%%US')
    print('%.1f%%\t%.1f%%' %
          (100 * N_UK / (N_UK + N_US), 100 * N_US / (N_US + N_UK)))
