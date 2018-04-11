# -*- coding: utf-8 -*-
from __future__ import print_function, division

import re
# Regex to detect URLs
#url_regex = re.compile('.*(https?://)?(www\\.)?([a-z0-9]+\\.)+(org|com|edu|be|ly|gl|co|tv|it|fm|net)(/[^/]*)*.*')
url_regex = re.compile('.*(https?://)?(www\\.)?([a-z0-9]+\\.)+(\w\w\w?)(/[^/]*)*.*')

# Language id
from langid.langid import LanguageIdentifier, model
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

def contains_url(s):
    """Check whether a string contains a url"""
    return bool(url_regex.match(s))

# Regex to strip markdown formatting
def strip_markdown(s):
    """Strip markdown formatting"""
    # Bold
    s = re.sub(r"\*\*(.*)\*\*", r"\1", s)
    # Italics
    s = re.sub(r"\*(.*)\*", r"\1", s)
    # Strikethrough
    s = re.sub(r"~~(.*)~~", r"\1", s)
    # Spoiler
    s = re.sub(r">!(.*)!<", r"\1", s)
    # Quote
    s = re.sub(r"^> ?(.*)", r"\1", s)
    # Inline code
    s = re.sub(r"`(.*)`", r"\1", s)
    # Code block
    s = re.sub(r"^( {4}|\t)+(.*)", r"\2", s)
    # Link
    s = re.sub(r"\[(.*)\]\((.*)\)", r"\1", s)
    
    return s


def normalize_punctuation(s):
    """Adapted from https://github.com/moses-smt/mosesdecoder/blob/master/scripts/tokenizer/normalize-punctuation.perl"""
    s = re.sub(r"\r", r"", s)
    # remove extra spaces
    s = re.sub(r"\(", r" \(", s)
    s = re.sub(r"\)", r"\) ", s)
    s = re.sub(r" +", r" ", s)
    s = re.sub(r"\) ([\.\!\:\?\;\,])", r"\)$1", s)
    s = re.sub(r"\( ", r"\(", s)
    s = re.sub(r" \)", r"\)", s)
    s = re.sub(r"(\d) \%", r"$1\%", s)
    s = re.sub(r" :", r":", s)
    s = re.sub(r" ;", r";", s)
    s = re.sub(r"„", r'"', s)
    s = re.sub(r"“", r'"', s)
    s = re.sub(r"”", r'"', s)
    s = re.sub(r"–", r"-", s)
    s = re.sub(r"—", r" - ", s)
    s = re.sub(r" +", r" ", s)
    s = re.sub(r"´", r"'", s)
    s = re.sub(r"([a-z])‘([a-z])", r"\1'\2", s)
    s = re.sub(r"([a-z])’([a-z])", r"\1'\2", s)
    s = re.sub(r"‘", r'"', s)
    s = re.sub(r"‚", r'"', s)
    s = re.sub(r"’", r'"', s)
    s = re.sub(r"''", r'"', s)
    s = re.sub(r"´´", r'"', s)
    s = re.sub(r"…", r"...", s)
    # French quotes
    s = re.sub(r" « ", r' "', s)
    s = re.sub(r"« ", r'"', s)
    s = re.sub(r"«", r'"', s)
    s = re.sub(r" » ", r'" ', s)
    s = re.sub(r" »", r'"', s)
    s = re.sub(r"»", r'"', s)
    # handle pseudo-spaces
    s = re.sub(r" \%", r"\%", s)
    s = re.sub(r"nº ", r"nº ", s)
    s = re.sub(r" :", r":", s)
    s = re.sub(r" ºC", r" ºC", s)
    s = re.sub(r" cm", r" cm", s)
    s = re.sub(r" \?", r"\?", s)
    s = re.sub(r" \!", r"\!", s)
    s = re.sub(r" ;", r";", s)

    s = re.sub(r", ", r", ", s)
    s = re.sub(r" +", r" ", s)

    # English "quotation," followed by comma, style
    re.sub(r'"([,\.]+)', r'\1"', s)

    re.sub(r"(\d) (\d)", r"$1.$2", s)

    return s

def replace_tabs_and_newlines(string):
    # Tab replaced by space
    string = re.sub(r'\t', " ", string)
    # Newlines replaced by space
    string = re.sub(r'\n', " ", string)
    
    return string

def is_not_language(string, lang='en'):
    actual_lang, prob = identifier.classify(string)
    return actual_lang != lang and prob > 0.5

if __name__ == '__main__':
    print(normalize_punctuation("“what’s up?”, he said"))
    test_url = 'www.reddit.com/r/something'
    print('%s is a url: %s' %(test_url, contains_url(test_url)))
