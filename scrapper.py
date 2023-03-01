
from bs4 import BeautifulSoup as bs
import requests   # importing requests module to open a URL
import pandas as pd
import openpyxl
df = pd.read_excel(r'C:\Users\c.gomez\Desktop\testMappe.xlsx')

number= '7SG1111-4AA01-0CA0'

def extract_source(number):
    url = 'https://mall.industry.siemens.com/mall/de/b1/Catalog/Product/' + number
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=headers).text
    soup = bs(source, 'html.parser')
    ProductInfo = soup.find("table", {"class": "ProductDetailsTable"})
   # print(ProductInfo)

    ls= list(ProductInfo)

    # Convert the filter object to list
   # print(ls. find('>EAN<'))
    #print(ls[45])
   # ean= ProductInfo.find(string=lambda t: "EAN" in t.text)

    for i in range ( 30 , 60):
        ean = ls[i].get_text()
        if "EAN" in ean:
            return(ean[5:18])



   # print( ean)

    return None
#urlopen = requests.get('https://mall.industry.siemens.com/mall/de/b1/Catalog/Product/3RH1921-1MA11').text

#soup = bs(urlopen,'html.parser')
#print(soup)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    list= df['Termingüte'].tolist()
    df.write_column('C2', list)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
