# scrapejs
Scraping JS rendered websites with Python.

## Installation
You will need to install the Python libraries in requirements.txt.
```
pip install -r requirements.txt
```
You will also need PhantomJS webdriver for selenium.
```
brew install phantomjs
```

## Configuration
- Enable Google Sheets API on your gmail account
- Download the json credentials to your computer and update the file path in the script
- On first run, you will be promopted to give permissions which will be stored in token.json
- Configure the API scope and the Google Sheet on config.json
