"""############## Simple Twitter listener + printout ##############

Installation like in README.md

* requires python3

* install using command:

pip3 install -r requirements.txt


* run from the repository's main directory using command:
sudo python3 -m erika.twitter



Troubleshooting:


FileNotFoundError: [Errno 2] No such file or directory: '/dev/ttyACM0'

* change the configured ERIKA_PORT to the right device / COM port


ModuleNotFoundError: No module named 'erika.local_settings'

* copy [erika3004]/erika/local_settings.py.template to [erika3004]/erika/local_settings.py and add the required credentials
"""
import string
from queue import Queue
from threading import Thread

from erika.local_settings import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from erika.local_settings import COMMA_SEPARATED_HASH_TAGS_TO_LISTEN_FOR
from erika.local_settings import ERIKA_MAX_LINE_LENGTH
from erika.local_settings import ERIKA_PORT
from twython import TwythonStreamer

from erika.erika import Erika


# simple twitter listener + printout to Erika device
#
# THIS MODULE NEEDS LOVE - add some proper tests, remove global state + make it look nice!


class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        if 'text' in data:
            username = data['user']['screen_name']
            tweet = data['text']
            tweet_as_string = "{}: {}".format(username, tweet)
            # print(tweet)
            q.put(tweet_as_string)

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


q = Queue()

# TODO bad style, use "with" statement instead for clean closing...
erika = Erika(ERIKA_PORT)


def twitter_worker():
    stream = MyStreamer(APP_KEY, APP_SECRET,
                        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=COMMA_SEPARATED_HASH_TAGS_TO_LISTEN_FOR)


def erika_worker():
    tweet_as_string = q.get(block=True)
    erika.crlf()
    print("### DEBUG (tweet):" + tweet_as_string)
    sanitized_tweet = tweet_as_string
    sanitized_tweet = ''.join(c for c in sanitized_tweet if c in (string.digits + string.ascii_letters + "@.,;: "))
    sanitized_tweet = sanitized_tweet.replace('@', "[at]")
    sanitized_tweet = sanitized_tweet[:ERIKA_MAX_LINE_LENGTH]
    print("### DEBUG (print string):" + sanitized_tweet)
    erika.print_ascii(sanitized_tweet)
    erika.crlf()


# block until all tasks are done
# q.join()

#####
# TODO: shutdown
# stop workers
# for i in range(num_worker_threads):
#    q.put(None)
# for t in threads:
#    t.join()
####

def main():
    threads = []
    t = Thread(target=twitter_worker)
    t.start()
    threads.append(t)

    t = Thread(target=erika_worker)
    t.start()
    threads.append(t)


if __name__ == "__main__":
    main()