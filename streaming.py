from slistener import SListener
import time, tweepy, sys

##Authentication
consumer_key = "HDJNJYmgnkecU87UvAWSwNDdK"
consumer_secret = "ADpOXeHvuh6uiG0xieweuCXEQD2a7UQqLEAuov1QTrwDhtRNkI"

access_token = "215905178-burCGOJ9LhFAIL4Um3DXB1luN4fYYMtMWPyIr5MM"
access_token_secret = "4lSni5fHILbZspY056rzhZSTWkgcCIglpuhlwuNKUQ3DH"


#Using the credentials for tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Start the streaming
api = tweepy.API(auth)

def main():
    track = ['hillary', 'clinton', 'trump', 'donald', 'election2016']
    languages = ["en"]
 
    listen = SListener(api, 'Twitter.Elections.Data')
    stream = tweepy.Stream(auth = api.auth, listener = listen)

    print "Streaming started..."

    try: 
        stream.filter(languages= languages, track = track)
    except:
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
    main()