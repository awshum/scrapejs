from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import stock

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SPREADSHEET_ID = '1RbdAn7mG-f8tGFyQrWsV2s1by-Tme7wOrjHTYeqaggA'
RANGE_NAME = 'Test!A2:Z'

def write_sheet(service, rows):
    """A function that will write to a Google Sheet. """
    body = {
        'values': rows
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')));

def append_sheet(service, rows):
    """A function that will append data to a Google Sheet table."""
    body = {
        'values': rows
    }
    value_input_option = 'USER_ENTERED'
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells appended.'.format(result.get('updates').get('updatedCells')));

def prepare_rows(tickers):
    print("preparing rows")
    rows = []
    for ticker in tickers:
        data = stock.Stock(ticker)
        data.get_data()
        rows.append([
            data.name, data.ticker, data.exchange, data.price, 
            data.shares, data.equity, data.revenue, data.net_income, 
            data.week52high, data.week52low, data.roe, data.roa, data.eps_ttm
        ])
    return rows


def main():
    # set up authentication with Google Sheets
    store = file.Storage('../token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME).execute()
    #values = result.get('values', [])
    #if not values:
    #    print('No data found.')
    #else:
    #    for row in values:
    #        print('%s, %s' % (row[0], row[1]))
    
    # Tickers set up here are passed as parameters for Stock objects.
    tickers = sorted([
        'FB', 'BABA', 'AAPL', 'AMZN', 'GOOG', 'CRM', 'JD', 'HEAR',
        'NFLX', 'SHOP', 'TSLA', 'WMT', 'MSFT', 'CRUS', 'BIDU'
    ])
    rows = prepare_rows(tickers)
    write_sheet(service, rows)

if __name__ == '__main__':
    main()
