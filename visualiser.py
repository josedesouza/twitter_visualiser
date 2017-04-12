
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime




class TwitterVisualiser(object):
    def __init__(self, path_to_data):
        # 1. Load in tweet file
        self.data = self.load_data()
        # 2. Parse tweets into dataframe
        self.tweets_df = self.create_tweet_dataframe(self.data)
        
    def load_data(self, path_to_data):
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
        return tweets_data
        
    def create_tweet_dataframe(self, tweets_data):
        tweets = pd.DataFrame()
        tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
        tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
        tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
        tweets['timestamp'] = map(lambda tweet: tweet['timestamp_ms'], tweets_data)
        tweets.set_index(pd.to_datetime(tweets['timestamp'],unit='ms'), inplace=True)
        tweets.drop('timestamp', inplace=True, axis=1)
        return tweets
    def plot_volume(self):
        # Plot volume of tweets over time
        tweets_df = self.tweets_df
        fig, ax = plt.subplots(1,1,figsize=(8,5))
        tweets_df[tweets_df.lang == 'en']['text'].groupby(pd.TimeGrouper(freq='1min')).count().plot(kind='line', ax=ax, label='en')
        tweets_df[tweets_df.lang == 'it']['text'].groupby(pd.TimeGrouper(freq='1min')).count().plot(kind='line', ax=ax, color='green', label='it')
        ax.set_title('Volume of Tennis-related tweets over time by country')
        ax.legend()
        ax.set_xlabel('Minute'); ax.set_ylabel('Volume of Tweets')
        plt.show()
        
    def plot_country(self):
        # PLOT Country
        tweets_df = self.tweets_df
        fig, ax = plt.subplots(1,1,figsize=(4,2))
        tweets_df['country'].value_counts().plot(ax=ax, kind='bar', 
                                                 title ='Tennis keyword tweets by country', 
                                                 alpha=0.6)
        plt.show()
        
    def plot_language(self):
        # PLot language
        fig, ax = plt.subplots(1,1,figsize=(6,3))
        tweets_df['lang'].value_counts().plot(ax=ax, kind='bar', 
                                                 title ='Tennis keyword tweets by Language', color='green')
        plt.show()                                         
                                                 
                                              
if __name__ == '__main__':
    data_path = './all_tennis_tweets.txt'
    visualiser = TwitterVisualiser(data_path)
    # DO plots
    visualiser.plot_volume()
    visualiser.plot_country()
    visualiser.plot_language()






