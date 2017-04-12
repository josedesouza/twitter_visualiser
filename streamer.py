from __future__ import print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import time
import sys
import numpy as np
import pandas as pd

# KEYS
consumer_key = 'EWewHQTcGltcQAY2rVMJ6T7ny'
consumer_secret = 'IlUGS6EKU41HyLcTOwQTGMnXzMnpUKy3sPh59RFm1vUO27GAnx'
access_token = '842723664936275969-r80UXaIMxX7M5o9LgoGoJxsHqIaU8p5'
access_token_secret = 'gcSVVhIhwYNcZERcpxrFLA4BPezHqrfyEuwHob4SvccNI'


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status
        
if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=['tennis', 'grand', 'slam'])