import sys
import string
import time
from tweepy import Stream
from tweepy.streaming import StreamListener
from twitter_client import get_twitter_auth
import io
import json

class CustomListener(StreamListener):
    """Custom StreamListener for streaming Twitter data."""

    def __init__(self, fname):
        safe_fname = format_filename(fname)
        self.outfile = "../gulf_twitter_raw/stream_%s.jsonl" % safe_fname
        
    def on_data(self, data):
        try:
            with io.open(self.outfile, 'a', encoding='utf8') as f:
                json.dumps(f.write(data))
                return True
        except BaseException as e:
            sys.stderr.write("Error on_data: {}\n".format(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n".format(status))
            time.sleep(15 * 60)
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True
        

def format_filename(fname):
    """Convert fname into a safe string for a file name.

    Return: string
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if "invalid".

    Return: string
    """
    invalid_chars = "-.%s%s" % (string.ascii_letters, string.digits)
    if one_char in invalid_chars:
        return '_'
    else:
        return one_char

if __name__ == '__main__':
    query = sys.argv[1:] # list of CLI arguments
    query_fname = ' '.join(query) # string
    auth = get_twitter_auth()
    twitter_stream = Stream(auth, CustomListener(query_fname))
    twitter_stream.filter(languages=["ar"], track=query, async=True)
