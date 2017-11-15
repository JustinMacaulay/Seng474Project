'''
tweetRetrieval.py
Stephanie Goodale
SENG 474 Project
11/10/2017

Use Twitter API and tweepy functions to access a chosen user's most 
recent tweets and write into a CSV file.  CSV format includes the 
tweet ID, the datetime that it was posted, and the text of the tweet.
Note: Twitter only allows access to a users most recent 3240 tweets.
'''

#!/usr/bin/env python
#encoding: utf-8

import tweepy
import csv
import html
 
#consumer keys and access tokens, used for OAuth Twitter API
consumer_key = 'XQCnw2YBIgJCDJthDT6AQTiPD'
consumer_secret = 'uYLZJNpJuViuxoTWcutdKN4pV6AjqW79Oqams6HmbDMDMuHGxz'
access_token = '928741549969514496-6ffPlRa6GJMwb7Ohwd3pNEBmm71TZhq'
access_token_secret = 'ZoKgBKjfJeZwZl2NYZdPKGyLIJIpB7eFd6lzfHFBau3u7'


def get_all_tweets(screen_name):
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode='extended')
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print('getting tweets before %s' % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, tweet_mode='extended')
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print('...%s tweets downloaded so far' % (len(alltweets)))
	
	#get extended tweets
	for tweet in alltweets:
		tweet.text = tweet.full_text
		tweet.text = html.unescape(tweet.text)
		
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w', encoding='utf_8_sig') as f:
		writer= csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("realDonaldTrump")


