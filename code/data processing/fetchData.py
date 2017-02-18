from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from processData import processData
from pymongo import MongoClient

#Google drive connection
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance

#Local File
fileName = './streaming_data/tweetData.json'
logFile = './logfile.txt'

#MongoDB connection
client = MongoClient()
db = client.tweet_db
collection = db.tweets_1500_End

# Auto-iterate through all files in the root folder.
file_list = drive.ListFile({'q': "'0B7ziEhBHYh1bc3hEREo1eS1fMWs' in parents and trashed=false"}).GetList()
#file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
start = 1500 + 179
total = len(file_list[start:])
i = 0
with open(logFile, 'w') as op:
    for f in file_list[start:]:
        i += 1
        print('File %d of %d (%d, %d)' % (i, total, start, len(file_list)))
        print('Title: %s' % (f['title']))
        op.write('\r\nTitle: ' + f['title'])
        f.GetContentFile(fileName)
        processedData = processData(fileName)
        processedData.process()
        result = collection.insert_many(processedData.getTweets())
        print('Tweets %d' % (len(result.inserted_ids)))
        op.write('\r\nTweets' + str(len(result.inserted_ids)))
print 'Completed All'
