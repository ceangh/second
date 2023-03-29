
from bs4 import BeautifulSoup as bs
import requests   # importing requests module to open a URL
import pandas as pd
import openpyxl
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_source(url):

    #print(number)
   # time.sleep(2)
   # url = 'https://r-stahl.com/de/global/suchergebnisse/?q='+ str(number) +'.html'


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


         print(soup)
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
             #print(str(number) + ' ' + ean_value)
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

def search(article_number):
    url = f'https://r-stahl.com/de/global/suchergebnisse/?q={article_number}'
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    link = soup.select_one('div.results-teaser a')['href']
    return 'https://r-stahl.com' + link


def extract_gtin(url):
    # Fetch the HTML content of the URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive'
    }

    response = requests.get(url, headers=headers)

    # Parse the HTML content using Beautiful Soup
    soup = bs(response.content, 'html.parser')



    return soup
# Press the green button in the gutter to run the script.



if __name__ == '__main__':
    #print(extract_source(search('220322')))

   # gtin = extract_gtin(search('220322'))
  #  print(gtin)

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # Navigate to the website containing the collapsed panel
    driver.get(search('220322'))

    # Find the button that expands the panel and click it
    expand_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[2]/section/div[2]/div/div/div[2]/div[12]/div[1]/h4")))
    expand_button.click()

    # Wait for the panel to expand and extract the data you need
    panel_data = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,
                                                                                 "/html/body/div[3]/div[2]/section/div[2]/div/div/div[2]/div[12]/div[2]/div")))
    print(panel_data)
    panel_text = panel_data.get_attribute('textContent')
    print(panel_text)
    panel_html = panel_data.get_attribute('innerHTML')

    # Close the browser window
    driver.quit()

    # Process the HTML code to extract the necessary data
    print(panel_html)
   # df = pd.read_excel(r'C:\Users\c.gomez\Desktop\input.xlsx',dtype={'Bestellnummer':str})
    # Apply function to column data and store result in new column
   # df['EAN'] = df['Bestellnummer'].apply(extract_source)

    # Save modified DataFrame to Excel file
   # df.to_excel('output_Eaton.xlsx', index=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
