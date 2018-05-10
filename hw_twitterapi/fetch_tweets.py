from __future__ import print_function
import json
import tweepy
import time

"""
Fetches tweets and creates a JSON file.
"""

tokens = open('twitter_key.txt')
# who's tweet will be collected
username = "ylecun"
# tweet limit to collect
tweet_limit = 5
# name of output JSON file
tweet_file = 'tweets.json'


# Assumes you have a file with name twitter_key.txt
# in this directory which stores tokens in this order
with open('twitter_key.txt') as f_in:
    consumer_key = f_in.readline().rstrip('\n')
    consumer_secret = f_in.readline().rstrip('\n')
    access_token = f_in.readline().rstrip('\n')
    access_token_secret = f_in.readline().rstrip('\n')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,
                 retry_count=5,
                 retry_delay=10,
                 retry_errors=set([401, 404, 500, 503]),
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

search = api.user_timeline(screen_name = username, count=100, include_rts=False)

counter = 0
with open(tweet_file, 'w+', encoding='utf8') as f_out:
    # It will store tweets like array in JSON file
    f_out.write('[\n')
    for status in search:
        for status in tweepy.Cursor(api.user_timeline, screen_name = username,
                                    include_rts = False).items():
            json.dump(status._json, f_out, ensure_ascii=False, indent=4)
            f_out.write('\n')
            counter += 1
            if counter == tweet_limit:
                f_out.write(']')
                # A hardcore exit, it would have been a soft one...
                exit()
            f_out.write(',')
    f_out.write(']')

print ("completed, total tweets=" + str(counter))
