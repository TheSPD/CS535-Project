from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def upload(argv):
		filename = argv[1]
		bucket_name, object_name = argv[2][5:].split('/', 1)
		assert bucket_name and object_name

		service = get_authenticated_service(RW_SCOPE)

		print ('Building upload request...')
		media = MediaFileUpload(filename, chunksize=CHUNKSIZE, resumable=True)
		if not media.mimetype():
		  media = MediaFileUpload(filename, DEFAULT_MIMETYPE, resumable=True)
		request = service.objects().insert(bucket=bucket_name, name=object_name,
		                                   media_body=media)

		print ('Uploading file: %s to bucket: %s object: %s ' % (filename, bucket_name,
		                                                        object_name))

		progressless_iters = 0
		response = None
		while response is None:
		  error = None
		  try:
		    progress, response = request.next_chunk()
		    if progress:
		      print_with_carriage_return('Upload %d%%' % (100 * progress.progress()))
		  except HttpError, err:
		    error = err
		    if err.resp.status < 500:
		      raise
		  except RETRYABLE_ERRORS, err:
		    error = err

		  if error:
		    progressless_iters += 1
		    handle_progressless_iter(error, progressless_iters)
		  else:
		    progressless_iters = 0

		print ('\nUpload complete!')

		print ('Uploaded Object:')
		print (json_dumps(response, indent=2))


def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
    upload(sys.argv)

if __name__ == '__main__':
    main()
