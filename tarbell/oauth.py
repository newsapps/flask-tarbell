from oauth2client import client
from oauth2client import keyring_storage
from oauth2client import tools
from apiclient import discovery
import getpass
import httplib2
import os
import argparse
import sys

OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive.file'

parser = argparse.ArgumentParser(description=__doc__,
         formatter_class=argparse.RawDescriptionHelpFormatter,
         parents=[tools.argparser])
flags = parser.parse_args(['--noauth_local_webserver'])

def get_drive_api(path, reset_creds=False):
    """
    Reads the local client secrets file if available (otherwise, opens a
    browser tab to walk through the OAuth 2.0 process, and stores the client
    secrets for future use) and then authorizes those credentials. Returns a
    Google Drive API service object.
    """
    # Retrieve credentials from local storage, if possible
    storage = keyring_storage.Storage('tarbell', getpass.getuser())
    credentials = None
    if not reset_creds:
        credentials = storage.get()
    if not credentials:
        flow = client.flow_from_clientsecrets(os.path.join(path, 'client_secrets.json'),
                                              scope=OAUTH_SCOPE)
        credentials = tools.run_flow(flow, storage, flags)
        storage.put(credentials)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('drive', 'v2', http=http)
    return service
