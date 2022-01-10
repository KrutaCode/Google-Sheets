import requests
import yahoo_fin.stock_info as si
from lxml import etree
from bs4 import BeautifulSoup


class Stock:
    def __init__(self,ticker,commodity=False):
        #Assign ticker to class member
        self.ticker = ticker
        self.error_count = 0

        #Assemble url
        self.url = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}&.tsrc=fin-srch"
        #If the asset can be found on Yahoo Finance, but not Google Finance
        if commodity:
            #Get the contents of the webpage
            self.webpage = requests.get(self.url)
            #Create soup object
            self.soup = BeautifulSoup(self.webpage.content,'html.parser')
            dom = etree.HTML(str(self.soup))
            self.price = si.get_live_price(self.ticker)
            self.price = self.formatNumber(self.price)
            self.pctChange = dom.xpath("/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[3]/div[1]/div/fin-streamer[3]/span/text()")
            try:
                self.pctChange = self.pctChange[0]
                self.pctChange = self.pctChange[1:-1]
                if "+" in self.pctChange:
                    self.pctChange = self.pctChange[1:]
            except IndexError:
                print(f"---Error Fetching Data---")
                self.pctChange = "N/A"

        #If the asset can be found on Google Finance
        else:
            #Fetch the data
            self.price = f'=GOOGLEFINANCE("{self.ticker}")'
            self.pctChange = f'=GOOGLEFINANCE("{self.ticker}","changepct")'

    ##########################
    # Function: getPrice()
    # Description: Returns the current price of the object(According to Yahoo finance)
    # Returns: String
    ##########################
    def getPrice(self):
        return self.price
    ##########################
    # Function: getPctChange()
    # Description: Returns the percent change of the asset or commodity.
    # Returns: String
    ##########################
    def getPctChange(self):
        return self.pctChange

    ##########################
    # Function: formatNumber()
    # Description: Returns a number formatted like a currency.
    # Returns: String
    ##########################
    def formatNumber(self, num):
        formattedNum = "{:,.2f}".format(num)
        return formattedNum
