from __future__ import print_function
import httplib2
import os
import errno

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import pandas as pd
import numpy as np

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def find_stocks():
    data_dir = os.path.join(os.getcwd(), 'dat')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return os.path.join(data_dir, 'stocks.yaml')

def list_to_df(values):
    header = values[0]
    df = {}
    for col in header:
        df[col] = []
    for row in values[1:]:
        if len(row) > 0:
            for key, val in zip(header, row):
                df[key].append(val)
    return pd.DataFrame(df)

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
class GApp():
    def __init__(self, myid):
        self.scopes = 'https://www.googleapis.com/auth/spreadsheets'
        self.jsonfile = os.path.join('.', 'credentials', 'client_id.json')
        self.app_name = 'Google Sheets Interface'
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        self.spreadsheetId = myid
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=myid).execute()
        sheets = sheet_metadata.get('sheets', '')[0]
        self.name = sheets['properties']['title']
        self.allrange = "{}!A1:ZZ".format(self.name)
        self.owner = sheets['properties']['title']

    def get_data(self, myrange):
        if len(myrange) == 0:
            thisrange = self.allrange
        else:
            thisrange = myrange
        result = self.service.spreadsheets().values().get(
        spreadsheetId=self.spreadsheetId, range=thisrange).execute()
        values = result.get('values', [])
        for row in values[1:]:
            how_many = len(values[0]) - len(row)
            for each in range(how_many):
                row.append('')
        clean_values = [[element or np.nan for element in row] for row in values]
        return clean_values

    def find_credentials(self):
        credential_dir = os.path.join(os.getcwd(), 'credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        return os.path.join(credential_dir, 'credentials.json')

    def get_credentials(self):
        credential_path = self.find_credentials()
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid: ### load credentials
            flow = client.flow_from_clientsecrets(self.jsonfile, self.scopes)
            flow.user_agent = self.app_name
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
