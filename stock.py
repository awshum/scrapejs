import requests
import json
from pprint import pprint

class Stock():
    """Each stock object represents an individual stock.
    Stock are initiated with a ticker."""
    def __init__(self, ticker):
        self.ticker = ticker

    def get_data(self):
        """Calls get_request with the IEXTrading API. 
        Adds results to attributes."""
        url = 'https://api.iextrading.com/1.0'
        j = self.get_request(url)
        data = json.loads(j)
        self.name = data['quote']['companyName']
        self.exchange = data['quote']['primaryExchange']
        self.price = data['quote']['latestPrice']
        self.equity = data['financials']['financials'][0]['shareholderEquity']
        self.revenue = data['financials']['financials'][0]['totalRevenue']
        self.net_income = data['financials']['financials'][0]['netIncome']
        self.eps_ttm = data['stats']['ttmEPS']
        self.shares = data['stats']['sharesOutstanding']
        self.week52high = data['stats']['week52high']
        self.week52low = data['stats']['week52low']
        self.roe = data['stats']['returnOnEquity']
        self.roa = data['stats']['returnOnAssets']
        print("Requesting quote for:", self.name)

    def get_request(self, url):
        """Makes a request for the ticker.
        Returns a JSON object"""
        endpoint = '/stock/{ticker}/batch?types=quote,financials,stats&period=annual'.format(ticker=self.ticker)
        response = requests.get("https://api.iextrading.com/1.0" + endpoint) 
        if response.status_code == 200:
            return response.content
        else:
            return None
        
if __name__ == "__main__":
    fb = Stock('FB')
    fb.get_data()
