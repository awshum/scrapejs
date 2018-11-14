from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SPREADSHEET_ID = '1a_I2ok0TGM95sKDncuUpPLCb3cTz1agcq8RsMPUvXCU'
RANGE_NAME = 'Sheet1!A:Z'

def write_sheet(service, rows):
    body = {
        'values': rows
    }
    result = service.spreadsheet().values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')));

def scrape():
    pass

def main():
    store = file.Storage('../token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME).execute()
    # Call scrape function
    # Write Outputs to sheet


if __name__ == "__main__":
    main()
