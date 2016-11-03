from tweepy import StreamListener
import json, time, sys

##Remove these lines
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
##Remove these lines

class SListener(StreamListener):

	def __init__(self, api = None, fprefix = 'streamer'):
		self.api = api or API()
		self.counter = 0
		self.fprefix = fprefix
		self.fileString = './streaming_data/' + fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json'
		self.output  = open(self.fileString, 'w')
		self.delout  = open('./streaming_data/' + 'delete.txt', 'a')
		##Remove these lines		
		self.gauth = GoogleAuth()
		self.gauth.LocalWebserverAuth()
		self.drive = GoogleDrive(self.gauth)
		##Remove these lines

		

	def on_data(self, data):

		if  'in_reply_to_status' in data:
			self.on_status(data)
		elif 'delete' in data:
			delete = json.loads(data)['delete']['status']
			if self.on_delete(delete['id'], delete['user_id']) is False:
				return False
		elif 'limit' in data:
			if self.on_limit(json.loads(data)['limit']['track']) is False:
				return False
		elif 'warning' in data:
			warning = json.loads(data)['warnings']
			print warning['message']
			return false

	def on_status(self, status):
		self.output.write(status + "\n")


		self.counter += 1

		if self.counter >= 20000:
			##Remove these lines
			file1 = self.drive.CreateFile()
			file1.SetContentFile(self.fileString)
			file1.Upload() # Files.insert()
			##Remove these lines
			self.output.close()
			self.fileString = './streaming_data/' + self.fprefix + '.' + str(time.strftime('%Y%m%d-%H%M%S')) + '.json'
			self.output = open(self.fileString, 'w')
			self.counter = 0

		return

	def on_delete(self, status_id, user_id):
		self.delout.write( str(status_id) + "\n")
		return

	def on_limit(self, track):
		sys.stderr.write(str(track) + "\n")
		return

	def on_error(self, status_code):
		sys.stderr.write('Error: ' + status_code + "\n")
		return False

	def on_timeout(self):
		sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
		time.sleep(60)
		return 
