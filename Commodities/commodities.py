import gspread
import requests
import yahoo_fin.stock_info as si
from bs4 import BeautifulSoup
from lxml import etree
from oauth2client.service_account import ServiceAccountCredentials

#A #B #C #D #E #F #G #H #I #J #K #L #M #N #O #P #Q #R #S #T #U #V #W #X #Y #Z
#1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

#Get credentials
creds = ServiceAccountCredentials.from_json_keyfile_name("creds/TradesCreds.json", scope)
#Create client object
client = gspread.authorize(creds)


class Stock:
    def __init__(self,ticker):
        #Assign ticker to class member
        self.ticker = ticker

        #Assemble url
        self.url = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}&.tsrc=fin-srch"

        #Get the contents of the webpage
        self.webpage = requests.get(self.url)

        #Create soup object
        self.soup = BeautifulSoup(self.webpage.content,'html.parser')
        dom = etree.HTML(str(self.soup))

        #Fetch the data
        self.price = dom.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[3]/div[1]/div/fin-streamer[1]/text()')
        self.pctChange = dom.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[3]/div[1]/div/fin-streamer[3]/span/text()')

        #Transfer to variable
        try:
            self.price = self.price[0]
            self.pctChange = self.pctChange[0]
        except IndexError:
            self.price = si.get_live_price(self.ticker)
            self.pctChange = '(0.0)'
            pass

        #Format the percentage
        self.pctChange = str(self.pctChange)
        self.pctChange = self.pctChange[1:-2]


        if "+" in self.pctChange:
            self.pctChange = self.pctChange[1:]

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


class Commodities:
    def __init__(self):
        self.sheet = client.open("Market Overview").sheet1
        commodity = {"Oil WTI":"MCL=F",
                     "Oil Brent":"BZ=F",
                     "Natural Gas":"NG=F",
                     "Gold":"GC=F",
                     "Silver":"SI=F",
                     "Copper":"HG=F",
                     "Palladium":"PA=F",
                     "Platinum":"PL=F",
                     "Aluminum":"ALI=F",
                     "Wheat US":"ZW=F",
                     "Steel":"^STEEL",
                     "Hot-Rolled Coils":"HRC=F",
                     "Sugar US":"SB=F",
                     "Coffee US":"KC=F",
                     "Cotton US":"CT=F",
                     "Cocoa US":"CC=F",
                     "Live Cattle":"LE=F",
                     "Lumber":"LBS=F"}
        #Gets the items of the dictionary
        dictionary_items = commodity.items()
        # Sorts the dictionary
        self.commodities = sorted(dictionary_items)

    def updateSpreadsheet(self):
        #The row to start entering the data on
        starting_row = 3
        #The column that contains the names
        names_col = 13
        #The column that contains the prices
        price_col = 14
        #The column that contains the percent change
        pctChance_col = 15
        row = starting_row

        for key,val in self.commodities:
            url = f"https://finance.yahoo.com/quote/{val}?p={val}&.tsrc=fin-srch"
            #Updates the cells the with the name and hyperlink.
            names_cell_value = self.sheet.cell(row,names_col).value
            if names_cell_value == None:
                self.sheet.update_cell(row, names_col, f'=HYPERLINK("{url}","{key}")')
            else:
                pass
            #Create stock object
            s = Stock(val)
            #Get the price
            price = s.getPrice()
            #Get the percent change
            pctChange = s.getPctChange()
            #Update the price
            self.sheet.update_cell(row, price_col, price)
            #Update the percent change
            self.sheet.update_cell(row, pctChance_col, pctChange)
            row += 1
    ##########################
    # Function: formatNumber()
    # Description: Returns a number formatted like a currency.
    # Returns: String
    ##########################
    def formatNumber(self,num):
        formattedNum = "{:,.2f}".format(num)
        return formattedNum


def main():
    c = Commodities()
    c.updateSpreadsheet()

main()
