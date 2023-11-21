#pip install requests beautifulsoup4

import requests
import pandas as pd
from bs4 import BeautifulSoup
urlMain = "https://catalogue.ite-expo.ru/ru-RU/exhibitorlist.aspx?project_id=495"  # ссылка на отрасль
requests.get(urlMain)
MainPages = requests.get(urlMain)
#print(MainPages)
# parser-lxml = Change html to Python friendly format
MainSoup = BeautifulSoup(MainPages.text, "lxml")  # код сайта готовый к обработки
soup = BeautifulSoup(MainPages.text, 'html.parser')
#print(MainSoup)

MainFilteredParsRes = MainSoup.find_all("a", class_="popUp")  # отфильтрованный код компаний
print(MainFilteredParsRes)

with open('PalpforTopPars.txt', "w") as f:
    CompanyName1 = []
    CompanyLink1 = []
    CompanyLink2 = []
    CompanyCountry = []
    CompanyDescriptionMass = []

    def topParser(filteredParsRes):
        for elem in filteredParsRes:
            CompanyFirstName = elem.find("div", class_="name")
            CompanyCountry = elem.find("div", class_="country")
            link_url = elem.get("href")
            print(CompanyFirstName.text)
            print(CompanyCountry.text)
            print("https://catalogue.ite-expo.ru"+link_url)
            CompanyLink1.append(CompanyFirstName.text + " ")
            CompanyCountry.append(CompanyCountry.text + " ")
            CompanyName1.append(CompanyFirstName.text + " ")
            print(" ")
        return CompanyLink1

    test = topParser(MainFilteredParsRes)

    ArrName = []
    ArrPhone1 = []
    ArrRegion = []
    ArrAdrress = []
    ArrContactPerson = []
    for elem in CompanyLink1:
        OneUrl = "https://catalogue.ite-expo.ru"
        pages = requests.get(OneUrl)
        # parser-lxml = Change html to Python friendly format
        soup = BeautifulSoup(pages.text, "lxml")  # код сайта готовый к обработки
        print(soup)