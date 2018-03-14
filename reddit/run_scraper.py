# -*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
import time

from scraper import RedditScraper


def main_loop(bot):
    """Main loop for the bot"""
    # Start looping
    i = 0
    bot.tick()
    for comment in bot.r_all.stream.comments():
        # Check if comment is and iambic pentameter
        done = bot.process_comment(comment)
        # If enough commebts have been processed, kill the procgram
        if done:
            exit()
        # Increment counter
        i += 1
        # Report periodically
        if i >= bot.options.report_every:
            # Print infos
            percent_noisy_comments = bot.n_noisy_comments / bot.n_comments * 100
            percent_noisy_strings = bot.n_noisy_strings / bot.n_strings * 100
            percent_bpe = bot.n_bpe_selected / bot.n_noisy_strings * 100
            percent_dic = bot.n_dic_selected / bot.n_noisy_strings * 100
            print('Analyzed %d comments, ' % bot.n_comments +
                  '%.2f%% contained noisy sentences, ' % percent_noisy_comments +
                  'found %d noisy strings ' % bot.n_noisy_strings +
                  '(bpe: %.2f%%, ' % percent_bpe +
                  'dic: %.2f%%), ' % percent_dic +
                  '%.1f comments/s' % (bot.n_comments / bot.tick()))
            sys.stdout.flush()
            # Reset counters
            # Sleep a bit
            time.sleep(bot.options.sleep_for)            # Reset periodic counters
            # Reset periodic counters
            self.reset_counts()
            i = 0

def main():
    # Instantiate bot
    bot = RedditIambicPentameterBot(sys.argv[1])
    # Run in while loop to recover from unknown exceptions
    while True:
        try:
            # Run main loop            main_loop(bot, subreddit)
            main_loop(bot)
        except Exception as e:
            print('Unknown error: ' + str(e), file=sys.stderr)


def test():
    bot = RedditScraper(sys.argv[1])
    # Get test comment
    test_comment = bot.r.comment(id='cqmldc6')
    # Custom iambic pentameter
    test_comment.body = 'And cafeteria of other crackers'
    # Test
    bot.is_iambic_pentameter(test_comment, tweet=False)


if __name__ == '__main__':
    if '--test' in sys.argv:
        test()
    else:
        main()
