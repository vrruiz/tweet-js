== tweet-js.py ==

A very simple parser for Twitter JSON archive file for Python 3.

- Download your Twitter archive file.
- Uncompress it.
- Check the path to the file tweet.js, which contains all the tweets.
- Execute the parser.

$ python3 tweet-js.py -f path/data/tweet.js

It will print the content of all tweets.

=== Filter by hashtag ===

$ python3 tweet-js.py -f path/data/tweet.js -t hashtag

It will print the content of the tweets with this hashtag.


=== Filter by date ===

The -s argument filters messages by start date and -e argument
filters messages by end date. They can be used together.

$ python3 tweet-js.py -f path/data/tweet.js -s 2019-01-01 -e 2020-01-01

