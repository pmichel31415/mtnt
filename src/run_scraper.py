# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
import time

from scraper import RedditScraper


def main_loop(reddit_scraper):
    """Main loop for the scraper"""
    # Start looping
    reddit_scraper.tick()
    for comment in reddit_scraper.r_all.stream.comments():
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
            main_loop(reddit_scraper)
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
