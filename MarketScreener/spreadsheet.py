import time
import stock
import gspread
import datetime as dt
from gspread.exceptions import APIError
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


class Sheet:
    def __init__(self,spreadsheet,data,commodity=False):
        self.commodity = commodity
        self.error_count = 0
        try:
            self.sheet = client.open(spreadsheet).sheet1
        except APIError:
            time.sleep(120)
            self.sheet = client.open(spreadsheet).sheet1
        self.data = data

    ##########################
    # Function: updateSpreadsheet(int,int,int)
    # Description: Updates at sectors column
    # Returns: None
    ##########################
    def updateSpreadsheet(self,nameCol,priceCol,pctCol):
        # The row to start entering the data on
        starting_row = 3
        #The row that the update will be placed
        update_row = 2
        # The column that contains the names
        names_col = nameCol
        # The column that contains the prices
        price_col = priceCol
        # The column that contains the percent change
        pctChance_col = pctCol
        row = starting_row

        for key, val in self.data:
            url = f"https://finance.yahoo.com/quote/{val}?p={val}&.tsrc=fin-srch"

            # Create stock object
            if self.commodity:
                s = stock.Stock(val,commodity=self.commodity)
            else:
                s = stock.Stock(val)
            # Get the price
            price = s.getPrice()
            # Get the percent change
            pctChange = s.getPctChange()

            # Gets the value of the cells
            names_cell_value = self.getData(row,names_col)
            price_cell_value = self.getData(row,price_col)
            pctChange_cell_value = self.getData(row,pctCol)

            # If the cell is empty or the current value does not match the key value.
            if names_cell_value == None or names_cell_value != key:
                # Updates the cells the with the name and hyperlink.
                self.updateCell(row, names_col, f'=HYPERLINK("{url}","{key}")')
            else:
                pass
            # If the cell is empty or the value in it does not match the new value
            if price_cell_value == None or price_cell_value != price:
                # Update the price
                self.updateCell(row, price_col, price)
            else:
                pass

            # If the cell is empty or the value in it does not match the new value
            if pctChange_cell_value == None or pctChange_cell_value != pctChange:
                # Update the percent change
                self.updateCell(row, pctChance_col, pctChange)
            else:
                pass
            row += 1
        print(f"---Finished updating the spreadsheet---")
        timestamp = dt.datetime.now()
        timestamp = str(timestamp)
        date,time = timestamp.split(" ")
        time,_ = time.split(".")
        formattedDate = date + " " + time
        self.updateCell(update_row,names_col,formattedDate)

    ##########################
    # Function: updateCell(int,int,string)
    # Description: Will attempt to update the cell at the specified coordinates with the data passed in the parameter.
    # Returns: None
    ##########################
    def updateCell(self, row, col, data):
        try:
            self.sheet.update_cell(row, col, data)
        except APIError:
            time.sleep(90)
            print(f"---Quote exceeded...   Attempt: {self.error_count}---")
            self.error_count += 1
            if self.error_count >= 5:
                self.error_count = 0
                return
            else:
                self.updateCell(row, col, data)
    ##########################
    # Function: getData(int,int)
    # Description: Will attempt to get the data at a specific coordinate
    # Returns: Cell value
    ##########################
    def getData(self,row,col):
        try:
            data = self.sheet.cell(row, col).value
            return data
        except APIError:
            time.sleep(90)
            print(f"---Quote exceeded...   Attempt: {self.error_count}---")
            self.error_count += 1
            if self.error_count >= 5:
                self.error_count = 0
                return
            else:
                self.getData(row,col)
