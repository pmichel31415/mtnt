# -*- coding: utf-8 -*-
import re

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

if __name__ == '__main__':
    print(normalize_punctuation("“what’s up?”, he said"))
