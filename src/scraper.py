# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import traceback
import pickle
import numpy as np

# Reddit API module
import praw
# Utility functions
import util
# Noise detector
import noise

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
        # Noise detector
        self.noise_detector = noise.NoiseDetector(config_file)
        # Print config
        self.noise_detector.print_config()
        # Initialize the reddit API
        self.init_reddit()

    def reset_counts(self):
        """Reset counts of strings/comments processed"""
        # Number of comments processed
        self.n_comments = 0
        # Number of noisy comments processed
        self.n_noisy_comments = 0
        # Number of strings processed
        self.n_strings = 0
        # Number of noisy strings detected
        self.n_noisy_strings = 0
        # Number of noisy string selected based on vocabulary
        self.n_dic_selected = 0
        # Number of noisy string selected based on bpe LM
        self.n_bpe_selected = 0

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


    def save_noisy_strings(self, comment, noisy_strings):
        """Saves verse to tsv file with some metadata"""
        with open(self.general.output_file, 'a+') as f:
            for noisy_string, score in noisy_strings:
                print('%s' % noisy_string +                         # actual string
                      '\t%.3f' % score +                            # LM score
                      '\t%d' % time.time() +                        # timestamp
                      '\t/u/%s' % comment.author +                  # author
                      '\t/r/%s' % comment.submission.subreddit +    # subreddit
                      '\t%s' % comment.submission.over_18 +         # nsfw tag
                      '\t%s' % comment.permalink,                   # permalink
                      file=f)


    def is_done(self):
        """Returns true if the scraper has found `max_records` noisy strings"""
        return self.n_noisy_strings >= self.options.max_records

    def should_report(self):
        """Report periodically"""
        return (self.n_comments + 1) % self.options.report_every == 0

    def report(self):
        """Report progress"""
        percent_noisy_comments = self.n_noisy_comments / self.n_comments * 100
        print('Analyzed %d comments, ' % self.n_comments +
              '%.2f%% contained noisy sentences, ' % percent_noisy_comments +
              'found %d noisy strings, ' % self.n_noisy_strings +
              '%.1f comments/s' % (self.n_comments / self.tick()))
        sys.stdout.flush()

    def process_comment(self, comment):
        """Processes a reddit comment object

        Returns True when no more comment should be processed"""
        username = '%s' % comment.author
        # Ignore the comment if t's from /r/AutoModerator
        if username == 'AutoModerator':
            return False
        # Ignore possible bots
        if 'bot' in username.lower():
            return False
        # Check for noisy sentences
        try:
            # Count comment as processed
            self.n_comments += 1
            # Get noisy strings from comment
            noisy_strings = self.noise_detector.get_noisy_strings(comment)
            # Save them to file
            self.save_noisy_strings(comment, noisy_strings)
            # Count noisy strings
            self.n_noisy_strings += len(noisy_strings)
            # Count noisy comments and save on reddit just in case
            if len(noisy_strings) > 0:
                self.n_noisy_comments += 1
                comment.save()
        except Exception as e:
            print("Failed to process comment: ", file=sys.stderr)
            traceback.print_exc()
        # Stop if max number of records is reached
        return self.is_done()
