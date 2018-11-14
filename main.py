from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def write_sheet(service, rows, spreadsheet_id, range_name):
    body = {
        'values': [rows]
    }
    print(service)
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')));

def scrape(url, xpath):
    driver = webdriver.PhantomJS()
    driver.get(url)
    element = driver.find_element(By.XPATH, xpath)
    return element.text

def main():
    with open('config.json', 'r') as f:
        config = json.loads(f.read())
        SCOPES = config[0]['SCOPES']
        SPREADSHEET_ID = config[0]['SPREADSHEET_ID']
    RANGE_NAME = 'Sheet1!A5'
    store = file.Storage('./token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('./credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    # Call scrape function
    value = [scrape('https://finance.yahoo.com/quote/%5ESTI', '//*[@id="quote-header-info"]/div[3]/div/div/span[1]')]
    # Write Outputs to sheet
    write_sheet(service, value, SPREADSHEET_ID, RANGE_NAME)

if __name__ == "__main__":
    main()
