# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
import time

from scraper import RedditScraper

def main_loop_old_comments(reddit_scraper):
    """Main loop for the scraper, collecting old comments"""
    # Start looping
    reddit_scraper.tick()
    # starting timestamp
    timestamp = if reddit_scraper.reddit.start_timestamp is None time.time() else reddit_scraper.reddit.start_timestamp
    # Collect posts on a day to day basis
    delta_time = 24*3600
    # Go back up to 2006 (reddit was funded in 2005)
    while timestamp > 1136073600:
        for submission in reddit_scraper.subreddit.submissions(start=timestamp-delta_time, end=timestamp):
            comments = submission.comments
            comments.replace_more(limit=None)
            for comment in comments.list():
                # Check if comment is contains noisy strings
                done = reddit_scraper.process_comment(comment)
                # If enough commebts have been processed, kill the program (R.I.P.)
                if done:
                    exit()
                # Report periodically
                if reddit_scraper.should_report():
                    # Print infos
                    reddit_scraper.report()
                    # Sleep a bit
                    time.sleep(reddit_scraper.options.sleep_for)
                    # Reset periodic counters
                    reddit_scraper.reset_counts()
        # Previous day
        timestamp -= delta_time


def main_loop_new_comments(reddit_scraper):
    """Main loop for the scraper, collecting new comments"""
    # Start looping
    reddit_scraper.tick()
    for comment in reddit_scraper.subreddit.comments(limit=None):
        # Check if comment is contains noisy strings
        done = reddit_scraper.process_comment(comment)
        # If enough commebts have been processed, kill the program (R.I.P.)
        if done:
            exit()
        # Report periodically
        if reddit_scraper.should_report():
            # Print infos
            reddit_scraper.report()
            # Sleep a bit
            time.sleep(reddit_scraper.options.sleep_for)
            # Reset periodic counters
            reddit_scraper.reset_counts()

def main():
    # Instantiate reddit_scraper
    reddit_scraper = RedditScraper(sys.argv[1])
    # Run in while loop to recover from unknown exceptions
    while True:
        try:
            # Run main loop
            if reddit_scraper.reddit.new_comments:
                main_loop_new_comments(reddit_scraper)
            else:
                main_loop_old_comments(reddit_scraper)
        except Exception as e:
            print('Unknown error: ' + str(e), file=sys.stderr)


def test():
    reddit_scraper = RedditScraper(sys.argv[1])
    # Get test comment
    test_comment = reddit_scraper.r.comment(id='cqmldc6')
    # Custom iambic pentameter
    test_comment.body = 'And cafeteria of other crackers'
    # Test
    reddit_scraper.process_comment(test_comment, tweet=False)


if __name__ == '__main__':
    if '--test' in sys.argv:
        test()
    else:
        main()
