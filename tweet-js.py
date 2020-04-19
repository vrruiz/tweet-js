#!/usr/bin/python3
import json

from optparse import OptionParser

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
                  help="Path to Twitter JSON archive.", metavar="FILE")
parser.add_option("-t", "--hashtag", dest="hashtag",
                  help="Filter by hashtag", metavar="HASHTAG")
(options, args) = parser.parse_args()

## Read Twitter file (JSON format)
tweets_js = read_twitter_json(options.filename)

## Loop over tweets
for tweet in tweets_js:
    # Decode tweet in a simple structure
    tweet_simple = tweet_decode(tweet)
    if options.hashtag:
        # Filter by hashtag
        if (options.hashtag in tweet_simple['hashtags']):
            print_tweet(tweet_simple)
    else:
        print_tweet(tweet_simple)

