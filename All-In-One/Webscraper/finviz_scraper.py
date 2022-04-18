# Data Manipulation
import pandas as pd

# Extracting Data
from bs4 import BeautifulSoup as bs
import requests

# GSHEET Object
import Google_Sheets.gsheet

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Upgrade-Insecure-Requests': '1', 'Cookie': 'v2=1495343816.182.19.234.142',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Referer': "http://finviz.com/quote.ashx?t="}


class FinViz_Scraper:
    def __init__(self):

        self.df = None

    '''
    Function: set_dataframe(DataFrame)
    Description: Creates a dataframe for the entire class  to manipulate. 
    Returns: None
    '''
    def set_dataframe(self, df: pd.DataFrame):
        self.df = df

    '''
    Function: set_fundamental_data(list,list)
    Description: Gets the data from Finviz and puts it into the dataframe
    Returns: None
    '''
    def set_fundamental_data(self):
        for symbol in self.df.index:
            try:
                r = requests.get(f"https://finviz.com/quote.ashx?t={symbol.lower()}", headers=headers)
                soup = bs(r.content, "html.parser")
                for m in self.df.columns:
                    self.df.loc[symbol, m] = self.get_metric_data(soup, m)
            except Exception:
                print(f"-- {symbol.upper()} was not found")
                # Since the data
                self.df = self.df.drop(symbol)


    '''
    Function: get_dataframe()
    Description: Retrieves the dataframe created by the class
    Returns: DataFrame
    '''
    def get_dataframe(self):
        return self.df

    '''
    Function: get_metric_data(BeautifulSoup, str)
    Description: Gets the data for the specific metric passed.
    Returns: Any
    '''
    @staticmethod
    def get_metric_data(soup, metric):
        class_of_element = "snapshot-td2"
        return soup.find(text=metric).find_next(class_=class_of_element).text

    '''
    Function: get_data_point(str, str)
    Description: This will retrieve a specific piece of data from the dataframe that was created earlier.  
    Returns: 
    '''

    def get_data_point(self, ticker, metric):
        return self.df.loc[ticker,metric]

    '''
    Function: 
    Description: 
    Returns: 
    '''

    '''
    Function: 
    Description: 
    Returns: 
    '''

    '''
    ### TODO
    1. Add google sheet functionality 

    '''


