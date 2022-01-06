import gspread
import time
import requests
import yahoo_fin.stock_info as si
from bs4 import BeautifulSoup
import pickle
from lxml import etree
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import APIError

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
        self.error_count = 0

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
        self.sheet = client.open("Market Screener").sheet1
        commodity = self.loadFromDB()
        self.error_count = 0

        # Sorts the dictionary
        self.commodities = sorted(commodity)

    ##########################
    # Function: updateSpreadsheet()
    # Description: Updates the commodity section of the spreadsheet with new data
    # Returns: None
    ##########################
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

            # Create stock object
            s = Stock(val)
            # Get the price
            price = s.getPrice()
            # Get the percent change
            pctChange = s.getPctChange()

            #Gets the value of the cells
            names_cell_value = self.sheet.cell(row, names_col).value
            price_cell_value = self.sheet.cell(row, price_col).value
            pctChange_cell_value = self.sheet.cell(row,pctChance_col).value

            # If the cell is empty or the value in it does not match the new value
            if names_cell_value == None or names_cell_value != key:
                # Updates the cells the with the name and hyperlink.
                self.updateCell(row, names_col, f'=HYPERLINK("{url}","{key}")')
            else:
                pass
            # If the cell is empty or the value in it does not match the new value
            if price_cell_value == None or price_cell_value != price:
                #Update the price
                self.updateCell(row, price_col, price)
            else:
                pass

            # If the cell is empty or the value in it does not match the new value
            if pctChange_cell_value == None or pctChange_cell_value != pctChange:
                #Update the percent change
                self.updateCell(row, pctChance_col, pctChange)
            else:
                pass
            row += 1
        print(f"---Finished updating the spreadsheet---")
    ##########################
    # Function: formatNumber()
    # Description: Returns a number formatted like a currency.
    # Returns: String
    ##########################
    def formatNumber(self,num):
        formattedNum = "{:,.2f}".format(num)
        return formattedNum
    ##########################
    # Function: updateCell(int,int,string)
    # Description: Will attempt to update the cell at the specified coordinates with the data passed in the parameter.
    # Returns: None
    ##########################
    def updateCell(self,row,col,data):
        try:
            self.sheet.update_cell(row,col,data)
        except APIError:
            time.sleep(90)
            print(f"---Quote exceeded...   Attempt: {self.error_count}---")
            self.error_count += 1
            if self.error_count >= 5:
                self.error_count = 0
                return
            else:
                self.updateCell(row,col,data)

    ##########################
    # Function: addToDB()
    # Description: Adds item to pickle file
    # Returns: None
    ##########################
    def addToDB(self, name, ticker):
        file = open("commodities.pkl", "wb")
        self.commodities.append((name, ticker))
        pickle.dump(self.commodities, file)
        file.close()
        print(f"---{ticker} was successfully added to the database---")
    ##########################
    # Function: loadFromDB()
    # Description: Loads data from a pickle file into a variable.
    # Returns: list of tuples
    ##########################
    def loadFromDB(self):
        file = open("commodities.pkl","rb")
        data = pickle.load(file)
        file.close()
        return data
    def removeFromDB(self,ticker):
        data = self.loadFromDB()
        new_data = []
        index = 0
        print(f"First:")
        for key,val in data:
            if val == ticker:
                del data[index]
            print(f"{val}")
            index += 1

        file = open("commodities.pkl","wb")
        pickle.dump(data,file)
        file.close()

def main():
    c = Commodities()
    c.updateSpreadsheet()

main()
