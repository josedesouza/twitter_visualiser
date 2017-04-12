import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class TwitterVisualiser(object):
    """Loads in a .txt file of tweets and parses into pandas dataframe for visualisation
       Can then visualise either tweet volume over time, country or language of the tweet"""
       
    def __init__(self, path_to_data):
        # 1. Load in tweet file
        self.data = self.load_data(path_to_data)
        # 2. Parse tweets into dataframe
        self.tweets_df = self.create_tweet_dataframe(self.data)
        
    def load_data(self, path_to_data):
        """ Load in tweet dump file """
        tweets_data_path = path_to_data
        tweets_data = []
        tweets_file = open(tweets_data_path, "r")
        for line in tweets_file:
            try:
                tweet = json.loads(line)
                tweets_data.append(tweet)
            except:
                continue
        return tweets_data
        
    def create_tweet_dataframe(self, tweets_data):
        """Parse tweets into pandas data frame"""
        tweets = pd.DataFrame()
        tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
        tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
        tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
        tweets['timestamp'] = map(lambda tweet: tweet['timestamp_ms'], tweets_data)
        tweets.set_index(pd.to_datetime(tweets['timestamp'],unit='ms'), inplace=True)
        tweets.drop('timestamp', inplace=True, axis=1)
        return tweets
    def plot_volume(self):
        """ Plot volume of tweets over time """
        tweets_df = self.tweets_df
        fig, ax = plt.subplots(1,1,figsize=(8,5))
        tweets_df[tweets_df.lang == 'en']['text'].groupby(pd.TimeGrouper(freq='1min')).count().plot(kind='line', ax=ax, label='en')
        tweets_df[tweets_df.lang == 'it']['text'].groupby(pd.TimeGrouper(freq='1min')).count().plot(kind='line', ax=ax, color='green', label='it')
        ax.set_title('Volume of Tennis-related tweets over time by country')
        ax.legend()
        ax.set_xlabel('Minute'); ax.set_ylabel('Volume of Tweets')
        plt.show()
        
    def plot_country(self):
        """ Plots summary of tweet country of origin"""
        tweets_df = self.tweets_df
        fig, ax = plt.subplots(1,1,figsize=(4,2))
        tweets_df['country'].value_counts().plot(ax=ax, kind='bar', 
                                                 title ='Tennis keyword tweets by country', 
                                                 alpha=0.6)
        plt.show()
        
    def plot_language(self):
        """ Plots summary of language of tweets"""
        tweets_df = self.tweets_df
        fig, ax = plt.subplots(1,1,figsize=(6,3))
        tweets_df['lang'].value_counts().plot(ax=ax, kind='bar', 
                                                 title ='Tennis keyword tweets by Language', color='green')
        plt.show()                                         
                                                 
                                              
if __name__ == '__main__':
    # 1. Create visualiser 
    data_path = './all_tennis_tweets.txt'
    visualiser = TwitterVisualiser(data_path)
    # 2. Make plots of loaded twitter data
    visualiser.plot_volume()
    visualiser.plot_country()
    visualiser.plot_language()






