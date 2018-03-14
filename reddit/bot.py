# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
import time

# Reddit API module
import praw
# Bindings to KenLM for the language model
import kenlm
# Utility functions
import util

class RedditScraper(object):
    """A bot selecting noisy sentences from reddit comments"""

    def __init__(self, config_file):
        """Init from yaml"""
        self.config_file = config_file
        util.load_config(self, config_file)
        # Reset counts
        self.reset_counts()
        # Start timer
        self.start = time.time()
        # Load dictionary
        with open(self.dictionary.dic_file, 'rb') as f:
            self.dic = pickle.load(f) 
        # Load language model
        self.lm = kenlm.Model(self.language_model.lmodel_file)
        # Get the percentile of length normalized scores we'll use as a threshold
        norm_train_scores = np.loadtxt(self.language_model.train_scores)[:,1]
        self.score_threshold = np.percentile(norm_train_scores, self.language_model.score_percentile)
        # Initialize the reddit API
        self.init_reddit()
        # Print config
        self.print_config()

    def reset_counts(self):
        """Reset counts of strings/comments processed"""
        # Number of comments processed
        self.n_comments = 0
        # Number of noisy comments processed
        self.n_comments = 0
        # Number of strings processed
        self.n_strings = 0
        # Number of noisy strings detected
        self.n_noisy_strings = 0
        # Number of noisy string selected based on vocabulary
        self.n_dic_selected = 0
        # Number of noisy string selected based on bpe LM
        self.n_bpe_selected = 0

    def print_config(self):
        if self.verbose:
            print('score_threshold: %.3f' % self.score_threshold)

    def init_reddit(self):
        # Get reddit instance
        self.r = praw.Reddit(user_agent=self.reddit.user_agent,
                             client_id=self.reddit.client_id,
                             client_secret=self.reddit.secret,
                             username=self.reddit.user_name,
                             password=self.reddit.password)
        # Get r/all/ instance
        self.r_all = self.r.subreddit(self.reddit.subreddit)

    def tick(self):
        """Get time since last call"""
        elapsed = time.time() - self.start
        self.start = time.time()
        return elapsed

    def preprocess_comment(self, comment):
        """Preprocess comment (essentially lowercase)"""
        return (comment.body).strip('\n').lower().split('\n')

    def has_bad_lm_score(self, candidate):
        """Check if comment is an iambic pentameter"""
        # Get scores from lm score
        score = self.lm.score(candidate, bos = True, eos = True)
        # Check whether the score is bad enough
        return score < self.score_threshold

    def contains_oovs(self, candidate):
        """Check whether a string contains OOV words"""
        has_oov = False
        # Iterate over all words in the candidate string
        for word in candidate.split():
            if not (word in self.dic):
                return True
        # If no OOV return False
        return False

    def get_noisy_strings(self, comment):
        """Select all 'noisy' strings in a reddit comment"""
        # Preprocess the comment to get a list of candidate lines
        candidates = self.preprocess_comment(comment)
        # list storing noisy sentences
        noisy_strings = [] 
        # Iterate over all lines in comment
        for candidate in candidates:
            # Only process strings over a certain number of characters
            if len(candidate) >= self.options.min_num_chars:
                # Check whether the comment has a bad lm score
                bad_score = self.has_bad_lm_score(candidate)
                # Check whether the sentence has OOVs
                oov = self.contains_oovs(candidate)
                # If both conditions are true then we have a good candidate
                if bad_score and oov:
                    self.n_noisy_strings += 1
                    noisy_strings.append(candidate)
                # Also count the number of candidates processed
                self.n_strings += 1
                self.n_bpe_selected += int(bad_score)
                self.n_dic_selected += int(oov)
        # Increment the number of comments processed
        self.n_comments += 1
        self.n_noisy_comments += int(len(noisy_strings) > 0)
        # Return noisy comments
        return noisy_strings

    def save_noisy_strings(self, comment, noisy_strings):
        """Saves verse to tsv file with some metadata"""
        with open(self.general.output_file, 'a+') as f:
            for noisy_string in noisy_strings:
                print('%s' % noisy_string +                         # actual string
                      '\t%d' % time.time() +                        # timestamp
                      '\t/u/%s' % comment.author +                  # author
                      '\t/r/%s' % comment.submission.subreddit +    # subreddit
                      '\t%s' % comment.submission.over_18 +         # nsfw tag
                      '\t%s' % comment.permalink,                   # permalink
                      file=f)


    def is_done(self):
        """Returns true if the bot has found `max_records` noisy strings"""
        return self.n_noisy_strings >= self.options.max_records

    def process_comment(self, comment):
        """Processes a reddit comment object

        Returns True when no more comment should be processed"""
        # Check for iambic pentameters
        try:
            # Get noisy strings from comment
            noisy_strings = self.get_noisy_strings(comment)
            # Save them to file
            self.save_noisy_strings(comment, noisy_strings)
            # Save comments on reddit just in case
            if len(noisy_strings) > 0:
                comment.save()
        except Exception as e:
            print("Failed to process comment: " + str(e), file=sys.stderr)
        # Stop if max number of records is reached
        return self.is_done()
