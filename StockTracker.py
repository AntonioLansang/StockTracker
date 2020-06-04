import requests
import bs4
import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'
        ]


#Put your file name within the quotes
credentials=ServiceAccountCredentials.from_json_keyfile_name('', scope)

gc = gspread.authorize(credentials)

#This is the whole Spreadsheet
SpreadSheet=gc.open('Investments- Value')

#This is to get the worksheet, the one with that has all the data
WorkSheet=SpreadSheet.worksheet('Data')

#This is a dummy line in order to see if cells update
WorkSheet.update_acell('B18', 'Gspread !')



def UpdatePrice(CurCell, x):
    #print(CurCell)


    #Finds the contents of the current cell "SPHD" "VOO" etc.
    StockSymbol= WorkSheet.acell(CurCell).value

    #This is the base URL used by all stocks on Yahoo Finance
    YahooFinURL="https://finance.yahoo.com/quote/"

    #Put them together to get the URL for the stock you want
    CompleteURL=YahooFinURL + StockSymbol

    #Re
    URLForStock=requests.get(CompleteURL)

    soup = bs4.BeautifulSoup(URLForStock.text, "html5lib")

    Price = soup.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    #print(Price)

    #D2
    UpdateThisCell='D'+str(x)
    #print(UpdateThisCell)

    WorkSheet.update_acell(UpdateThisCell, Price)


def main():
    for x in range(2,16):
        CurrentStock=('B'+str(x)) #Cell "B1" "B2" and so on
        UpdatePrice(CurrentStock, x)



if __name__== "__main__":
    main()



