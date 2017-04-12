
import json
import numpy as np
import pandas as pd


# Load in tweet dump file
tweets_data_path = './all_tennis_tweets.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
        
from datetime import datetime
def create_tweet_dataframe(tweets_data):
    tweets = pd.DataFrame()
    tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
    tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
    tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
    tweets['timestamp'] = map(lambda tweet: tweet['timestamp_ms'], tweets_data)
    tweets.set_index(pd.to_datetime(tweets['timestamp'],unit='ms'), inplace=True)
    tweets.drop('timestamp', inplace=True, axis=1)
    
    return tweets
tweets_df = create_tweet_dataframe(tweets_data)
tweets_df.head()