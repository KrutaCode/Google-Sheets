# Data Manipulation
import pandas as pd

# Extracting Data
from bs4 import BeautifulSoup as bs
import requests

# For date manipulation
import datetime as dt
from dateutil.relativedelta import relativedelta


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Upgrade-Insecure-Requests': '1', 'Cookie': 'v2=1495343816.182.19.234.142',
    'Accept-Encoding': 'gzip, deflate, sdch'}


class YahooFinanceScraper:
    def __init__(self,ticker):
        # Main ticker
        self.ticker = ticker.upper()

        # Option to add additional tickers
        self.ticker_list = [ticker]

        self.profitability = None
        self.management_effectiveness = None
        self.income_statement = None
        self.balance_sheet = None
        self.cash_flow_statement = None
        self.stock_price_history = None
        self.share_statistics = None
        self.dividends_and_split = None
        self.statistics_table = None
        self.income_statement_dataframe = None
        self.balance_sheet_dataframe = None
        self.cash_flow_dataframe = None
        self.price_dataframe = None



    '''
    Function: set_statistics_page()
    Description: Creates a dataframe for the entire class  to manipulate. 
    Returns: None
    '''
    def set_statistics_page(self):

                       # Profitability
        detailed_metric_list = ["Profit Margin", "Operating Margin",
                       # Management Effectiveness
                       "Return on Assets", "Return on Equity",
                       # Income Statement
                       "Revenue", "Revenue Per Share", "Quarterly Revenue Growth",
                       "Gross Profit", "EBITDA", "Net Income Avi to Common",
                       "Diluted EPS", "Quarterly Earnings Growth",
                       # Balance Sheet
                       "Total Cash", "Total Cash Per Share", "Total Debt", "Total Debt/Equity",
                       "Current Ratio", "Book Value Per Share",
                       # Cash Flow Statement
                       "Operating Cash Flow", "Levered Free Cash Flow",
                       # Stock Price History
                       "52-Week Change", "52 Week High",
                       "52 Week Low", "50-Day Moving Average", "200-Day Moving Average",
                       # Share Statistic
                       "Avg Vol (3 month)", "Avg Vol (10 day)", "Shares Outstanding",
                       "Implied Shares Outstanding", "Float", "% Held by Insiders",
                       "% Held by Institutions",
                       # Dividend & Splits
                       "Forward Annual Dividend Rate", "Forward Annual Dividend Yield",
                       "Trailing Annual Dividend Rate", "Trailing Annual Dividend Yield",
                       "5 Year Average Dividend Yield",
                       "Payout Ratio", "Dividend Date", "Ex-Dividend Date",
                       "Last Split Factor", "Last Split Date"]

        # Table from yahoo financial page
        table_metric_list = ["Market Cap (intraday)", "Enterprise Value", "Trailing P/E",
                             "Forward P/E", "PEG Ratio (5 yr expected)", "Price/Sales",
                             "Price/Book", "Enterprise Value/Revenue", "Enterprise Value/EBITDA"]

        # Class element for elements in the table on the financial page
        statistics_table_element = "Ta(c) Pstart(10px) Miw(60px) Miw(80px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor)"
        # Class element for elements below table on financial page
        statistics_page_element = "Fw(500) Ta(end) Pstart(10px) Miw(60px)"
        
        
        self.df = pd.DataFrame(index=self.ticker_list,columns=detailed_metric_list)

        soup_tracker = {'':''}

        for symbol in self.df.index:
            try:
                r = requests.get(f"https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}", headers=headers)
                soup = bs(r.content, "html.parser")
                soup_tracker[symbol] = soup
                for m in self.df.columns:
                    self.df.loc[symbol, m] = self.get_metric_data(soup, m, statistics_page_element)
            except Exception:
                print(f"-- {symbol.upper()} was not found")
                # Since the data
                self.df = self.df.drop(symbol)



        # Ranges for each field
        profitability_range = detailed_metric_list[0:2]
        management_effectiveness_range = detailed_metric_list[2:4]
        income_statement_range = detailed_metric_list[4:12]
        balance_sheet_range = detailed_metric_list[12:18]
        cash_flow_statement_range = detailed_metric_list[18:20]
        stock_price_history_range = detailed_metric_list[20:25]
        share_statistics_range = detailed_metric_list[25:32]
        dividend_and_splits_range = detailed_metric_list[32:42]

        self.profitability = pd.DataFrame(index=self.ticker_list, columns=profitability_range)
        self.management_effectiveness = pd.DataFrame(index=self.ticker_list, columns=management_effectiveness_range)
        self.income_statement = pd.DataFrame(index=self.ticker_list, columns=income_statement_range)
        self.balance_sheet = pd.DataFrame(index=self.ticker_list, columns=balance_sheet_range)
        self.cash_flow_statement = pd.DataFrame(index=self.ticker_list, columns=cash_flow_statement_range)
        self.stock_price_history = pd.DataFrame(index=self.ticker_list, columns=stock_price_history_range)
        self.share_statistics = pd.DataFrame(index=self.ticker_list, columns=share_statistics_range)
        self.dividends_and_split = pd.DataFrame(index=self.ticker_list, columns=dividend_and_splits_range)
        self.statistics_table = pd.DataFrame(index=self.ticker_list, columns=table_metric_list)



        # Fill each dataframe
        # Financials Table
        for symbol in self.profitability.index:
            for m in table_metric_list:
                self.statistics_table.loc[symbol, m] = self.get_metric_data(soup_tracker[symbol], m, statistics_table_element)

        # Profitability section
        for symbol in self.profitability.index:
            for m in detailed_metric_list[0:2]:
                self.profitability.loc[symbol,m] = self.get_metric_data(soup_tracker[symbol], m, statistics_page_element)

        # Management Effectiveness section
        for symbol in self.management_effectiveness.index:
            for m in detailed_metric_list[2:4]:
                self.management_effectiveness.loc[symbol,m] = self.get_metric_data(soup_tracker[symbol], m, statistics_page_element)

        # Income Statement
        for symbol in self.income_statement.index:
            for m in detailed_metric_list[4:12]:
                self.income_statement.loc[symbol,m] = self.get_metric_data(soup_tracker[symbol], m, statistics_page_element)

        # Balance Sheet
        for symbol in self.balance_sheet.index:
            for m in detailed_metric_list[12:18]:
                self.balance_sheet.loc[symbol,m] = self.get_metric_data(soup_tracker[symbol], m, statistics_page_element)

        # Cash flow statement
        for symbol in self.cash_flow_statement.index:
            for m in detailed_metric_list[18:20]:
                self.cash_flow_statement.loc[symbol, m] = self.get_metric_data(soup_tracker[symbol], m, statistics_page_element)

        # Stock price history
        for symbol in self.stock_price_history.index:
            for m in detailed_metric_list[20:25]:
                self.stock_price_history[symbol,m] = self.get_metric_data(soup_tracker[symbol], m, statistics_page_element)

        # Share Statistics
        for symbol in self.share_statistics.index:
            for m in detailed_metric_list[25:32]:
                self.share_statistics.loc[symbol, m] = self.get_metric_data(soup_tracker[symbol], m, statistics_page_element)

        # Dividends & Splits
        for symbol in self.share_statistics.index:
            for m in detailed_metric_list[32:42]:
                self.dividends_and_split.loc[symbol, m] = self.get_metric_data(soup_tracker[symbol], m, statistics_page_element)


    '''
    Function: set_income_statement()
    Description: 
    Returns: DataFrame
    '''
    def set_income_statement(self):

        # All the metrics that will be collected
        table_metric_list = ["Total Revenue", "Cost of Revenue", "Gross Profit",
                             "Operating Expense", "Operating Income", "Net Non Operating Interest Income Expense",
                             "Other Income Expense","Pretax Income", "Tax Provision",
                             "Net Income Common Stockholders", "Diluted NI Available to Com Stockholders", "Basic EPS",
                             "Diluted EPS", "Basic Average Shares", "Diluted Average Shares",
                             "Total Operating Income as Reported", "Total Expenses", "Net Income from Continuing & Discontinued Operation",
                             "Normalized Income", "Interest Income", "Interest Expense",
                             "Net Interest Income", "EBIT", "EBITDA",
                             "Reconciled Cost of Revenue", "Reconciled Depreciation", "Net Income from Continuing Operation Net Minority Interest",
                             "Normalized EBITDA"]

        # Class element for the table
        table_element = "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)"

        # Assigning the dataframe
        self.income_statement_dataframe = pd.DataFrame(index=self.ticker_list, columns=table_metric_list)

        for symbol in self.income_statement_dataframe.index:
            try:
                r = requests.get(f"https://finance.yahoo.com/quote/{symbol}/financials?p={symbol}", headers=headers)
                soup = bs(r.content, "html.parser")
                for m in self.income_statement_dataframe.columns:
                    self.income_statement_dataframe.loc[symbol, m] = self.get_metric_data(soup, m, table_element)
            except Exception:
                print(f"-- {symbol.upper()} was not found")
                # Since the data
                self.income_statement_dataframe = self.income_statement_dataframe.drop(symbol)

    '''
    Function: set_balance_sheet()
    Description: Scrapes the balance sheet and stores the values in a dataframe.
    Returns: None
    '''
    def set_balance_sheet(self):

        balance_sheet_metrics = ["Total Assets", "Total Liabilities Net Minority Interest", "Total Equity Gross Minority Interest",
                                 "Total Capitalization", "Common Stock Equity", "Net Tangible Assets",
                                 "Working Capital", "Invested Capital", "Tangible Book Value",
                                 "Total Debt", "Net Debt", "Share Issued", "Ordinary Shares Number"]

        # Class element for the table
        table_element = "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)"

        # Assigning the dataframe
        self.balance_sheet_dataframe= pd.DataFrame(index=self.ticker_list, columns=balance_sheet_metrics)

        for symbol in self.balance_sheet_dataframe.index:
            try:
                r = requests.get(f"https://finance.yahoo.com/quote/{symbol}/balance-sheet?p={symbol}", headers=headers)
                soup = bs(r.content, "html.parser")
                for m in self.balance_sheet_dataframe.columns:
                    self.balance_sheet_dataframe.loc[symbol, m] = self.get_metric_data(soup, m, table_element)
            except Exception:
                print(f"-- {symbol.upper()} was not found")
                # Since the data
                self.balance_sheet_dataframe = self.balance_sheet_dataframe.drop(symbol)

    '''
    Function: set_cash_flow_statement()
    Description: Scrapes the cash flow statement from yahoo.
    Returns: None
    '''
    def set_cash_flow_statement(self):

        cash_flow_metrics = ["Operating Cash Flow", "Investing Cash Flow", "Financing Cash Flow",
                             "End Cash Position", "Income Tax Paid Supplemental Data", "Interest Paid Supplemental Data",
                             "Capital Expenditure", "Issuance of Capital Stock", "Issuance of Debt",
                             "Repayment of Debt", "Repurchase of Capital Stock", "Free Cash Flow"]

        # Class element for the table
        table_element = "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)"

        # Assigning the dataframe
        self.cash_flow_dataframe = pd.DataFrame(index=self.ticker_list, columns=cash_flow_metrics)
        
        # Fill the dataframe
        for symbol in self.cash_flow_dataframe.index:
            try:
                r = requests.get(f"https://finance.yahoo.com/quote/{symbol}/balance-sheet?p={symbol}", headers=headers)
                soup = bs(r.content, "html.parser")
                for m in self.cash_flow_dataframe.columns:
                    self.cash_flow_dataframe.loc[symbol, m] = self.get_metric_data(soup, m, table_element)
            except Exception:
                print(f"-- {symbol.upper()} was not found")
                # Since the data
                self.cash_flow_dataframe = self.cash_flow_dataframe.drop(symbol)

    '''
    Function: set_price_data()
    Description:
    Returns: 
    '''
    def set_price_data(self):
        
        # Assigning the dataframe
       # self.price_dataframe = pd.DataFrame(index=self.ticker_list)

        dud = self.subtract_dates(4)

        print(f"DUD: {dud}")

        # Fill the dataframe
        for symbol in self.ticker_list:
            r = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={self.subtract_dates(5)}&period2={dt.datetime.now().timestamp()}&interval=1d&events=history&includeAdjustedClose=true"

            df = pd.read_csv(r)

            print(f"DF: {df}")
        
        

    '''
    Function: subtract_dates(int)
    Description: Subtracts a specified amount of years by the current date
    Returns: str
    '''
    def subtract_dates(self, years_to_subtract: int):
        new_time = dt.datetime.now() - relativedelta(years=years_to_subtract)
        print(f"New: {int(new_time.timestamp())}")
        return int(new_time.timestamp())


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
    Function: get_metric_data(BeautifulSoup, str)
    Description: Gets the data for the specific metric passed.
    Returns: Any
    '''
    @staticmethod
    def get_metric_data(soup, metric: str, class_of_element: str):
        data = soup.find(text=metric).find_next(class_=class_of_element).text
        return data

def main():

    ticker = "AAPL"

    yf = YahooFinanceScraper(ticker)
    yf.set_price_data()



main()
