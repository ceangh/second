# This is a sample Python script.
from bs4 import BeautifulSoup as bs
import requests   # importing requests module to open a URL
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
url= 'https://mall.industry.siemens.com/mall/de/b1/Catalog/Product/3RH1921-1MA11'

def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=headers).text
    soup = bs(source, 'html.parser')
    ProductInfo = soup.find("table", {"class": "ProductDetailsTable"})
   # print(ProductInfo)
    print("---------------------")
    ls= list(ProductInfo)

    # Convert the filter object to list
   # print(ls. find('>EAN<'))
    print(ls[45])
    print(ProductInfo.find_all(string=lambda t: "EAN" in t.text))

    return source
#urlopen = requests.get('https://mall.industry.siemens.com/mall/de/b1/Catalog/Product/3RH1921-1MA11').text

#soup = bs(urlopen,'html.parser')
#print(soup)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    extract_source(url)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
