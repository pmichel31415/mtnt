#!/usr/bin/python3
"""
Count the number of emojis in the input
"""
import sys
import emoji
import re

txt_emoji_regex = re.compile(r'(8|:|;|=)(\^|\'|-)?(\)|\(|D|P|p)')
utf8_emoji_regex = emoji.get_emoji_regexp()


N = 0
try:
    for line in sys.stdin:
        for w in line.strip().split():
            if txt_emoji_regex.search(w) or utf8_emoji_regex.search(w):
                N += 1
except (KeyboardInterrupt, EOFError):
    pass
finally:
    print(N)
