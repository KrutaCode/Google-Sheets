import os
import spreadsheet
import databases.pickleDatabase
import pathlib
path = os.getcwd() + "\\databases\\region.pkl"
file = pathlib.Path(path)
#Case for computer
if file.exists():
    DB_FILE = path
#Case for Rapsberry pi
else:
    DB_FILE = os.getcwd() + "/GoogleSpreadsheet/databases/region.pkl"

class RegionalTrackers:
    def __init__(self):
        self.pkl = databases.pickleDatabase.Database(DB_FILE)
        self.data = self.pkl.getData()
        self.data = sorted(self.data)
        self.Gspread = spreadsheet.Sheet("Market Screener",self.data)
        self.Gspread.updateSpreadsheet(5,6,7)


def main():
    r = RegionalTrackers()

main()
