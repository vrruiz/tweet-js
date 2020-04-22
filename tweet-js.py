#!/usr/bin/python3
import datetime
import json
import pytz

from dateutil.parser import parse
from optparse import OptionParser

utc = pytz.UTC

def read_twitter_json(file_name):
    """ Read JSON file and returns a json object"""
    with open(file_name, "r") as tweets_file:
        tweets_lines = tweets_file.readlines()
    # Replace header
    tweets_lines[0] = tweets_lines[0].replace('window.YTD.tweet.part0 = ', '')
    # Convert list back to text
    tweets_data = ''.join(tweets_lines)
    # Parse JSON twitter data
    tweets_js = json.loads(tweets_data)
    return tweets_js

def tweet_decode(tweet):
    """ Gets data from tweet and returns a simplified data structure
        tweet = {
            'full_text': 'This is a tweet #hello #world http://t.co/13456',
            'urls': [ 'http://en.wikipedia.org/' ]
            'hashtags': [ '#hello', '#world' ]
        }
    """
    tweet_simple = {}
    # Get data from tweet
    tweet_simple['full_text'] = tweet['tweet']['full_text'] # Text
    tweet_simple['created_at'] = tweet['tweet']['created_at'] # Text
    tweet_simple['datetime'] = parse(tweet_simple['created_at']) # Parse date to datetime

    # Initialize
    tweet_simple['hashtags'] = [] # List
    tweet_simple['urls'] = [] # URLs

    # Process hashtags
    hashtags = tweet['tweet']['entities']['hashtags'] # List of dictonaries
    for tag in hashtags:
        tweet_simple['hashtags'].append(tag['text'])

    # Process URLs
    urls = tweet['tweet']['entities']['urls'] # List of dictionaries
    for url in urls:
        tweet_simple['urls'].append(url['expanded_url'])

    return tweet_simple

def print_tweet(tweet):
    print("\"\"\"{}\"\"\"".format(tweet['full_text']))

## Parse options
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="Path to Twitter JSON archive.", metavar="FILENAME")
parser.add_option("-t", "--hashtag", dest="hashtag",
                  help="Filter by hashtag", metavar="HASHTAG")
parser.add_option("-g", "--list-hashtags", action="store_true",
                  dest="list_hashtags",
                  help="List the hashtags", metavar="LIST_HASHTAGS")
parser.add_option("-s", "--date-start", dest="date_start",
                  help="List the hashtags", metavar="LIST_HASHTAGS")
parser.add_option("-e", "--date-end", dest="date_end",
                  help="List the hashtags", metavar="LIST_HASHTAGS")

(options, args) = parser.parse_args()

# Validate dates
if (options.date_start):
    date_start = utc.localize(parse(options.date_start))
if (options.date_end):
    date_end = utc.localize(parse(options.date_end))

## Read Twitter file (JSON format)
tweets_js = read_twitter_json(options.filename)

## Variable initialization
hashtags = []

## Loop over tweets
for tweet in tweets_js:
    # Decode tweet in a simple structure
    tweet_simple = tweet_decode(tweet)
    if options.date_start:
        if tweet_simple['datetime'] <= date_start:
            continue
    if options.date_end:
        if tweet_simple['datetime'] >= date_end:
            continue

    if options.hashtag:
        # Filter by hashtag
        if (options.hashtag in tweet_simple['hashtags']):
            print_tweet(tweet_simple)
    elif (options.list_hashtags):
        for tag in tweet_simple['hashtags']:
            if (not tag in hashtags):
                hashtags.append(tag)
    else:
        print_tweet(tweet_simple)

## List hashtags
if (options.list_hashtags):
    for tag in hashtags:
        print(tag)
