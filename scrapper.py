
from bs4 import BeautifulSoup as bs
import requests   # importing requests module to open a URL
import pandas as pd
import openpyxl
import time

def extract_source(number):

    print(number)
    time.sleep(2)
    url = 'https://mall.industry.siemens.com/mall/de/b1/Catalog/Product/' + number
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=headers).text
    soup = bs(source, 'html.parser')
    ProductInfo = soup.find("table", {"class": "ProductDetailsTable"})
    ls= list(ProductInfo)

    for i in range ( 30 , 60):
        ean = ls[i].get_text()
        if "EAN" in ean:
            print(ean)
            return(ean[5:18])

    return None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    df = pd.read_excel(r'C:\Users\c.gomez\Desktop\input.xlsx')
    # Apply function to column data and store result in new column
    df['EAN'] = df['Bestellnummer'].apply(extract_source)

    # Save modified DataFrame to Excel file
    df.to_excel('output4.xlsx', index=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
