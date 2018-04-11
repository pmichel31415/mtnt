# -*- coding: utf-8 -*-
from __future__ import print_function, division

import numpy as np
import yaml
import re


class Attributes(object):
    """A class to access dict fields like object attributes"""

    def __init__(self, dic):
        self.__dict__.update(dic)


def load_config(obj, config_file):
    """Create fields from yaml file"""
    with open(config_file, 'r') as f:
        data = yaml.load(f)
        for k, v in data.items():
            obj.__dict__[k] = Attributes(v)


def load_wordlist(filename):
    """Load a list of word from a file (one word per line)"""
    words = []
    with open(filename, 'r') as f:
        for line in f:
            words.append(line.strip().lower())
    return words


def softmax(x):
    """Computes :math:`\frac{e^{x_i}}{\sum_je^{x_j}}`"""
    e = np.exp(x)
    return e / np.sum(e)

def savetxt(filename, txt):
    """Save list of strings to file"""
    with open(filename, 'w+') as f:
        for l in txt:
            print(l, file=f)
            
def loadtxt(filename):
    """Read list fo strings from file"""
    txt = []
    with open(filename, 'r') as f:
        for l in f:
            txt.append(l.strip())
    return txt
