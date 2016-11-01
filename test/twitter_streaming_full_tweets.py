import tweepy
import json, time, sys

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
	
	def __init__(self, api=None):
		self.api = api
		self.counter = 0
		self.fprefix = 'Election.Tweeets'
		self.output  = open('./streaming_data/' + self.fprefix + '.' 
			+ time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')

	def on_status(self, status):
		self.output.write((status))
		self.counter += 1
		print self.counter
		if self.counter >= 200:
			self.output.close()
			self.output = open('./streaming_data/' + self.fprefix + '.' 
				+ time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
			self.counter = 0
		return
				

	def on_error(self, status_code):
		if status_code == 420:
			#returning False in on_data disconnects the stream
			return False

#Credentials 
consumer_key = "HDJNJYmgnkecU87UvAWSwNDdK"
consumer_secret = "ADpOXeHvuh6uiG0xieweuCXEQD2a7UQqLEAuov1QTrwDhtRNkI"

access_token = "215905178-burCGOJ9LhFAIL4Um3DXB1luN4fYYMtMWPyIr5MM"
access_token_secret = "4lSni5fHILbZspY056rzhZSTWkgcCIglpuhlwuNKUQ3DH"


#Using the credentials for tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Start the streaming
api = tweepy.API(auth)
myStreamListener = MyStreamListener(api)
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

#filter
myStream.filter(languages = ["en"], track=['trump'])


# from nltk.twitter import Twitter
# tw = Twitter()
# tw.tweets(keywords='love, hate', limit=10) #sample from the public stream