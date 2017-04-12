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


class StreamRecorder(StreamListener):
    """Records incoming twitter stream data to file and handles errors"""
    def __init__(self, output_loc,output_loc_geo, location=None, timeout=None):
        """ - location: if specified, only write tweets that are from specific location"""
        self.start_time = time.time()
        self.limit = timeout
        super(StreamRecorder, self).__init__()
        self.output_loc = output_loc
        self.output_loc_geo = output_loc_geo
        self.location = location
        self.geo_tweet_count = 0 
        self.all_tweet_count = 0
    def on_data(self, raw_data):
        """Appends tweets to dump file""" 
        if (time.time() - self.start_time) < self.limit:
            data = json.loads(raw_data)
            if data['coordinates'] is not None:
                with open(self.output_loc_geo, 'a') as f:
                    f.write(raw_data)
                with open(self.output_loc, 'a') as f:
                    f.write(raw_data)
                self.geo_tweet_count +=1
                self.all_tweet_count +=1

            else:
                with open(self.output_loc, 'a') as f:
                    f.write(raw_data)
                self.all_tweet_count+=1
            return True
        else:
            # Timeout reached so stop stream
            return False
        
        
    def on_error(self, status_code):
        print (sys.stderr, 'Encountered error with status code:', status_code)
        sys.stdout.flush()
        return False # Don't kill the stream
    
    def on_timeout(self):
        return False
    
class TwitterStreamer(StreamListener):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, timeout=None):
        #This handles Twitter authetification and the connection to Twitter Streaming API
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.start_t = time.time()

        
        
    def start(self, keywords=['Tennis', 'tennis'], 
              output_loc='all_tennis_tweets.txt',
              output_loc_geo ='geo_tennis_tweets.txt',
             timeout=None):
        #This line filter Twitter Streams to capture data by the keywords
        self.start_t = time.strftime("%y-%m-%d %H:%M")
        print ("[%s] Starting the streaming..."%(self.start_t))
        self.stream = Stream(auth = self.auth,
                             listener = StreamRecorder(output_loc,output_loc_geo, timeout=timeout), 
                             timeout=timeout)

        self.stream.filter(track=keywords)
        
    def stop(self):
        self.end_t = time.strftime("%y-%m-%d %H:%M")
        print ("[%s] Ending the streaming..."%(self.end_t))
        self.stream.disconnect()
        
if __ name__ == '__main__':
    # RUN TO START RECORDING
    RUN_TIME = 100000 # How long you want the streamer to run in SECONDS
    streamer = TwitterStreamer(consumer_key, consumer_secret, access_token, access_token_secret, timeout= RUN_TIME)
    streamer.start(timeout= RUN_TIME)