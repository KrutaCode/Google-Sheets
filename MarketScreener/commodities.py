import os
import spreadsheet
import databases.pickleDatabase
import pathlib

path = os.getcwd() + "\\databases\\commodities.pkl"
file = pathlib.Path(path)
#Case for computer
if file.exists():
    DB_FILE = path
#Case for Rapsberry pi
else:
    DB_FILE = os.getcwd() + "/GoogleSpreadsheet/databases/commodities.pkl"

class Commodities:
    def __init__(self):
        self.pkl = databases.pickleDatabase.Database(DB_FILE)
        self.data = self.pkl.getData()
        self.data = sorted(self.data)
        self.Gspread = spreadsheet.Sheet("Market Screener",self.data,commodity=True)
        self.Gspread.updateSpreadsheet(13,14,15)

def main():
    #c = Commodities()
    pass
main()
