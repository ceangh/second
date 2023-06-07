import urllib3
from bs4 import BeautifulSoup as bs
import requests   # importing requests module to open a URL
import pandas as pd
import openpyxl
import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import threading

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time



def extract_source(number):

    print(number)
    time.sleep(2)
    url = 'https://mall.industry.siemens.com/mall/es/ES/Catalog/Product/?mlfb=' + str(number) + '&SiepCountryCode=ES'

    save_dir = 'C:/Users/c.gomez/Downloads'
    save_dir2 = 'C:/Users/c.gomez/PycharmProjects/pythonProject/SIEMENSPDF'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive'
    }

    s = requests.Session()  # Inicia una sesión de navegación
    response = s.get(url, headers=headers)  # Usa esa sesión para obtener la página

    if response.status_code == 200:
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir",
                               save_dir)  # Cambia esto a la ruta donde quieres guardar el PDF
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        profile.set_preference("pdfjs.disabled", True)  # Desactiva el visualizador de PDF integrado

        # Configura el driver de Selenium
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), firefox_profile=profile)

        driver.get(
            'https://mall.industry.siemens.com/mall/es/ES/Catalog/Product/?mlfb=6SL3244-0BB13-1FA0&SiepCountryCode=ES')

        driver.implicitly_wait(10)

        iframe = driver.find_element(By.XPATH, '//iframe[@id="iframe_id"]')
        driver.switch_to.frame(iframe)
        # Luego, busca el botón de aceptar todas las cookies
        accept_all_button = driver.find_element(By.CLASS_NAME, 'sc-eDvSVe')

        # Haz clic en el botón para aceptar todas las cookies
        accept_all_button.click()

        # Espera un poco para que la página cargue
        time.sleep(5)

        # Localiza el enlace del PDF y haz clic en él
        pdf_link = driver.find_element(By.CLASS_NAME, 'pdfLink')
        pdf_link.click()

        # Espera un poco para que el PDF se descargue
        time.sleep(5)

        driver.quit()

        # Obtén la lista de archivos en el directorio de descarga
        files = os.listdir(save_dir)

        # Encuentra el archivo descargado más reciente (puede que necesites ajustar esto si el servidor usa un esquema de nombres de archivos extraño)
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(save_dir, x)))

        # Crea la ruta completa al archivo descargado
        downloaded_file = os.path.join(save_dir, latest_file)

        # Crea la ruta completa al nuevo archivo con el nombre que deseas
        new_file = os.path.join(save_dir2, 'CDS_ES_' + str(number) + '.pdf')

        # Renombra el archivo descargado
        os.rename(downloaded_file, new_file)





            # Navega hasta la página


            # Si la solicitud fue exitosa
            # if pdf_response.status_code == 200:
            #     pdf_data = pdf_response.content
            #
            #     # Guarda el archivo PDF
            #     with open(os.path.join(save_dir, 'CDS_ES_' + str(number) + '.pdf'), 'wb') as f:
            #         f.write(pdf_data)


         # ean_value = None
         # spec_table = soup.find('div',
         #                        {'id': '0'})  # Find the table with id=0 which contains the General specifications
         # if spec_table:
         #     rows = spec_table.find_all('div', class_='module-table__row')
         #     for row in rows:
         #         cols = row.find_all('div', class_='module-table__col')
         #         if len(cols) == 2 and cols[0].text.strip() == 'EAN':
         #             ean_value = cols[1].text.strip()
         #             break
         # if ean_value:
         #     print(str(number) + ' ' + ean_value)
         #     return(ean_value)
         # else:
         #     return('NOT FOUND')
    # hier können Sie mit BeautifulSoup auf den Inhalt der Seite zugreifen
        return "CDS_ES_" + str(number) + ".pdf"
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
    #extract_source('6SL3244-0BB13-1FA0')
    df = pd.read_excel(r'C:\Users\c.gomez\Desktop\input.xlsx',dtype={'Bestellnummer':str})
    # Apply function to column data and store result in new column
    df['Ausgabe'] = df['Bestellnummer'].apply(extract_source)

    # Save modified DataFrame to Excel file
    df.to_excel('output_siemens_datenblätter', index=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
