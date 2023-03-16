
from bs4 import BeautifulSoup as bs
import requests   # importing requests module to open a URL
import pandas as pd
import openpyxl
import time

def extract_source(number):

    #print(number)
    time.sleep(2)
    url = 'https://www.eaton.com/us/en-us/skuPage.'+ str(number) +'.html'


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
         soup = bs(response.content, 'html.parser')
         ean_value = None
         spec_table = soup.find('div',
                                {'id': '0'})  # Find the table with id=0 which contains the General specifications
         if spec_table:
             rows = spec_table.find_all('div', class_='module-table__row')
             for row in rows:
                 cols = row.find_all('div', class_='module-table__col')
                 if len(cols) == 2 and cols[0].text.strip() == 'EAN':
                     ean_value = cols[1].text.strip()
                     break
         if ean_value:
             print(str(number) + ' ' + ean_value)
             return(ean_value)
         else:
             return('NOT FOUND')
    # hier können Sie mit BeautifulSoup auf den Inhalt der Seite zugreifen
    else:
         print('Die Anforderung war nicht erfolgreich. Fehlercode:', response.status_code)
  #  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

   # source=requests.get(url, headers=headers).text
    #soup = bs(source, 'html.parser')
   # print(soup)
   # ProductInfo = soup.find("table", {"class": "ProductDetailsTable"})
  #  if ProductInfo is None:
  #      return 'NOT FOUND'

  #  ls= list(ProductInfo)

  #  for i in range ( 30 , 60):
   #     ean = ls[i].get_text()
    #    if "EAN" in ean:
     #       print(ean)
      #      return(ean[5:18])

    return None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   # extract_source(184765)
    df = pd.read_excel(r'C:\Users\c.gomez\Desktop\input.xlsx')
    # Apply function to column data and store result in new column
    df['EAN'] = df['Bestellnummer'].apply(extract_source)

    # Save modified DataFrame to Excel file
    df.to_excel('output_Eaton.xlsx', index=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
