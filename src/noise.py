# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pickle
import numpy as np

# Moses tokenizer
from nltk.tokenize.moses import MosesTokenizer
# Bindings to KenLM for the language model
import kenlm
# Bindings to sentencepiece for sub-words
import sentencepiece
# Various text processing procedures
import text
# Utility functions
import util

class NoiseDetector(object):
    """Retrieve noisy text from comments"""

    def __init__(self, config_file):
        """Init from yaml"""
        self.config_file = config_file
        util.load_config(self, config_file)
        # Load dictionary
        with open(self.dictionary.dic_file, 'rb') as f:
            self.dic = pickle.load(f) 
        # Moses tokenizer
        self.moses_tokenizer = MosesTokenizer(self.options.language)
        # Load subword tokenizer
        self.subword_tokenizer = sentencepiece.SentencePieceProcessor()
        self.subword_tokenizer.Load(self.subwords.model_file)
        # Load language model
        self.lm = kenlm.Model(self.language_model.model_file)
        # Get the percentile of length normalized scores we'll use as a threshold
        norm_train_scores = np.loadtxt(self.language_model.train_scores)[:,1]
        self.score_threshold = np.percentile(norm_train_scores, self.language_model.score_percentile)
    
    def print_config(self):
        """Print infos that weren't specified before runtime"""
        if self.general.verbose:
            print('score_threshold: %.3f' % self.score_threshold)
            sys.stdout.flush()

    def preprocess_candidate(self, candidate):
        """Preprocess comment (essentially lowercase and tokenizes with Moses tokenizer)"""
        # Remove mqrkdown
        candidate = text.strip_markdown(candidate)
        # normalize punctuation
        normalized_candidate = text.normalize_punctuation(candidate)
        # Tokenize
        if self.options.language != 'ja':
            tokenized_candidate = self.moses_tokenizer.tokenize(normalized_candidate, return_str=True)
        else:
            tokenized_candidate = normalized_candidate
        # Lowercase
        lowercased_candidate = tokenized_candidate.lower()
        return lowercased_candidate


    def has_bad_lm_score(self, candidate):
        """Check if the candidate sentence has a bad score under the language model"""
        # Split into subwords
        pieces = self.subword_tokenizer.EncodeAsPieces(candidate)
        tokenized_candidate = ' '.join(pieces)
        # Get scores from lm score
        score = self.lm.score(tokenized_candidate, bos=True, eos=True) #min(self.lm.score(' '.join(five_gram), bos=True, eos=True) for five_gram in pieces[::5])
        # Normalize by length
        normalized_score = score / (len(pieces) + 1e-20)
        # Check whether the score is bad enough
        return normalized_score < self.score_threshold, normalized_score

    def contains_oovs(self, candidate):
        """Check whether the candidate sentence contains OOV words"""
        # For japanese, return True (because OOVs is too restrictive)
        if self.options.language == 'ja':
            return True
        # Else check for OOVs
        has_oov = False
        # Iterate over all words in the candidate string
        words = candidate.split()
        for word in words:
            if not (word in self.dic):
                return True
        # If no OOV return False
        return False

    def get_noisy_strings(self, comment):
        """Select all 'noisy' strings in a reddit comment and returns them with their LM scores"""
        # Get comment body
        body = comment.body.strip('\n')
        # Split into lines
        lines = body.split('\n')
        # list storing noisy sentences
        noisy_strings = [] 
        # Iterate over all lines in comment
        for line in lines:
            # Preprocess (tokenize, lowercase)
            candidate = self.preprocess_candidate(line)
            # Only process strings over a certain number of characters
            if len(candidate) >= self.options.min_num_chars:
                # Check whether the comment has a bad lm score
                bad_score, score = self.has_bad_lm_score(candidate)
                # Check whether the sentence has OOVs
                oov = self.contains_oovs(candidate)
                # If both conditions are true then we have a good candidate
                if bad_score and oov:
                    noisy_strings.append((line, score))
        # Return noisy comments
        return noisy_strings
