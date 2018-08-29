#!/usr/bin/python3
"""
This is a glorified `grep -Ff` that counts the number of words from stdin
that are contained in a list of keywords
"""
import sys

keywords = set()
with open(sys.argv[1], 'r') as swf:
    for l in swf:
        keywords.add(l.strip())

N = 0
try:
    while True:
        line = input()
        for w in line.strip().split():
            if w in keywords:
                N += 1
except (KeyboardInterrupt, EOFError):
    pass
finally:
    print(N)
