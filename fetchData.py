from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from processData import processData
from pymongo import MongoClient

# Google drive connection
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Local File
fileName = './streaming_data/tweetData.json'
logFile = './logfile.txt'

# MongoDB connection
client = MongoClient()
db = client.tweet_db
collection = db.tweets

# Auto-iterate through all files in the root folder.

query = {'q': "'0B7ziEhBHYh1bc3hEREo1eS1fMWs' in parents and trashed=false"}
# query = {'q': "'root' in parents and trashed=false"}
file_list = drive.ListFile(query).GetList()
total = len(file_list)
i = 0
with open(logFile, 'w') as op:
    for f in file_list:
        i += 1
        print('File %d of %d' % (i, total))
        print('Title: %s' % (f['title']))
        op.write('\r\nTitle: ' + f['title'])
        f.GetContentFile(fileName)
        processedData = processData(fileName)
        processedData.process()
        result = collection.insert_many(processedData.getTweets())
        print('Tweets %d' % (len(result.inserted_ids)))
        op.write('\r\nTweets' + str(len(result.inserted_ids)))
print 'Completed All'
