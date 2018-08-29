#!/usr/bin/env python3
"""Counts the ratio between UK and US version of words

Looks at ise/ize
"""
import sys
import re

# Detects -ise/-ize words
ise_regex = re.compile(r'\w+is(e|ation|ing)s?$', re.I)
ize_regex = re.compile(r'\w+iz(e|ation|ing)s?$', re.I)

N_UK = N_US = 0
try:
    for line in sys.stdin:
        for w in line.strip().split():
            if ise_regex.search(w):
                N_UK += 1
            elif ize_regex.search(w):
                N_US += 1
except (KeyboardInterrupt, EOFError):
    pass
finally:
    uk_percent = 100 * N_UK / (N_UK + N_US)
    us_percent = 100 * N_US / (N_UK + N_US)
    print(f"UK  \tUS")
    print(f"{uk_percent:.1f}%\t{us_percent:.1f}%")
