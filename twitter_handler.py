import tweepy
import csv
import html

class twitter_handler():
    auth = None
    tweepy = None

    def __init__(self,app):
    	#authorize twitter, initialize tweepy
    	self.auth = tweepy.OAuthHandler(app.config["CONSUMER_KEY"], app.config["CONSUMER_SECRET"])
    	self.auth.set_access_token(app.config["ACCESS_TOKEN"], app.config["ACCESS_TOKEN_SECRET"])
    	self.api = tweepy.API(self.auth)

    def retrieve_tweet(self, tweet_id):
        tweet = self.api.get_status(id=tweet_id)
        return tweet
