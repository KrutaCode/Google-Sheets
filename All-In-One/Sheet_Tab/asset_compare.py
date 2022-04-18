# For data parsing
import pandas as pd
# For accessing the google sheet
from Google_Sheets.gsheet import Sheet
# Create object to scrape data
import Webscraper.finviz_scraper
# Get the metric list
from Webscraper.finviz_default_parameters import default_metric_list


# Where the placement starts at.
STATIC_ROW = 4
STATIC_COLUMN = 2


'''
Function:
Description:
Returns:
'''
def asset_compare():
    # Gets the number of assets that the user would like to compare.
    compare_quantity = int(input("-------------\n-How many assets would you like to compare?: "))

    # List to hold the tickers that the user enters
    ticker_list = []

    # Creates a sheet object on the page "Asset Compare"
    sheet = Sheet("Asset Compare")

    # Creates a finviz object for scraping
    finviz = Webscraper.finviz_scraper.FinViz_Scraper()

    # Index for while loop.
    index = 0

    print('\n')
    # Gets the user input of the tickers
    while index < compare_quantity:
        ticker_input = str(input(f"{index + 1}. |-Enter a ticker: "))
        ticker_list.append(ticker_input)

        index += 1

    # Create a dataframe with the tickers as the index, and the metric points are the columns.
    df = pd.DataFrame(index=ticker_list, columns=default_metric_list)

    finviz.set_dataframe(df)
    finviz.set_fundamental_data()

    # Dataframe with all of the scraped data
    new_df = finviz.get_dataframe()



    sheet.update_sheet(new_df)



















'''
Function:
Description:
Returns:
'''





