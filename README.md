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


