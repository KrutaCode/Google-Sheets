import pickle


class Database:
    def __init__(self,file):
        self.file = file
        try:
            with open(self.file,"rb") as f:
                self.currentData = pickle.load(f)
        except EOFError:
            self.currentData = []
        print(f"Current: {self.currentData}")
    ##############################
    # Function:
    # Description:
    # Returns:
    ##############################
    def createFile(self):
        dummyData = [('0','0')]
        with open(self.file) as f:
            pickle.dump(dummyData,f)
    ##############################
    # Function:
    # Description:
    # Returns:
    ##############################
    def addEntry(self,name,ticker):
        duplicate = self.isDuplicate(ticker)
        self.currentData.append((name,ticker))
        if duplicate:
            print(f"---{ticker} is already in the database---")
        else:
            with open(self.file,"wb") as f:
                pickle.dump(self.currentData,f)
            print(f"---{ticker} was successfully added to the database---")
    ##############################
    # Function:
    # Description:
    # Returns:
    ##############################
    def isDuplicate(self,ticker):
        for key,val in self.currentData:
            if ticker == val:
                return True
        return False

    ##############################
    # Function:
    # Description:
    # Returns:
    ##############################
    def getData(self):
        return self.currentData

    ##############################
    # Function:
    # Description:
    # Returns:
    ##############################
    def removeEntry(self,ticker):
        index = 0
        for key,val in self.currentData:
            if ticker == val:
                del self.currentData[index]
                break
            index += 1
        with open(self.file,"wb") as f:
            pickle.dump(self.currentData,f)
        print(f"---Successfully removed {ticker}---")
