import requests
import pandas as pd
from bs4 import BeautifulSoup

# https://www.youtube.com/watch?v=EF9UNlB05Rk&list=PL6plRXMq5RADYaw4Xo111smBcEPNMhdHf&index=3
# по другому гайду    https://idatica.com/blog/parsing-saytov-na-python-rukovodstvo-dlya-novichkov/  https://pishuverno.ru/kak-napisat-parser-dlya-sajta-na-python/
# Define URL
url = "https://tara.unipack.ru/russia-1063-ampuli"
requests.get(url)
pages = requests.get(url)
# parser-lxml = Change html to Python friendly format
soup = BeautifulSoup(pages.text, "lxml")  # код сайта готовый к обработки
filteredParsRes = soup.find_all("div",
                                class_="product-section")  # product-section simple,   отфильтрованный код компаний

with open('filteredParsResults.txt', "w") as f:
    CompanyName1 = []
    CompanyName2 = []
    CompanyLink1 = []
    CompanyLink2 = []
    CompanyPlaceMass = []
    CompanyDescriptionMass = []
    for elem in filteredParsRes:
        Links = elem.find_all("a")
        CompanyDescription = elem.find("p")
        CompanyPlace = elem.find("p", class_="product-p")
        f.write(
            " _________________________________________________________________________________________________________ \n")
        # print(elem.prettify())
        for link in Links:
            link_url = link.get("href")
            link_text = link.text.strip()
            link_title = link.get("title")
            # if (link_title!= None): f.write(link_title, end=' ')
            if link == Links[0]:
                if link_title != None: f.write(link_title)
                f.write(f" \n{link_text}\n{link_url}\n")
                CompanyName1.append(link_title + " ")
                CompanyName2.append(link_text + " ")
                CompanyLink1.append(link_url)
            if link == Links[-1]: CompanyLink2.append(link_url + " ")
        f.write(f"Место: {CompanyPlace.text}\n")
        f.write(f"Описание: {CompanyDescription.text}\n")
        CompanyPlaceMass.append(CompanyPlace.text + " ")
        CompanyDescriptionMass.append(CompanyDescription.text + " ")

# print (filteredParsRes)
# with open ("resultParsing.txt", "w", encoding = "utf-8") as file:     file.write(str (filteredParsRes))

# print(CompanyName1)
# print(CompanyLink1)
# print(CompanyPlaceMass)
# print(CompanyDescriptionMass)
NUM = len(CompanyPlace)
ArrName = []
ArrPhone1 = []
ArrCountry = []
ArrRegion = []
ArrAdrress = []
ArrContactPerson = []

with open('AlternateResults.txt', "w") as AlterF:
    for elem in CompanyLink1:  # проход по всем страницам компаний
        AlterF.write("________________________________________________________________________ \n")
        url = "https:" + elem + "/contacts"
        requests.get(url)
        pages = requests.get(url)
        # parser-lxml = Change html to Python friendly format
        soup = BeautifulSoup(pages.text, "lxml")  # код сайта готовый к обработки
        ContactSoup = soup.find("div", class_="block")  # product-section simple,   отфильтрованный код компаний
        ContactTableSoup = soup.find("table",
                                     class_="table mt20 table-company")  # product-section simple,   отфильтрованный код компаний
        if ContactSoup != None:  # если подробный сайт
            StrAdvanced = ContactSoup.text
            # StrAdvanced = StrAdvanced.replace("Контакты", "")    #замена в строке
            NameIndex = StrAdvanced.find("Контакты\n\n")
            AdrrIndex = StrAdvanced.find("Адрес: ")
            PhoneIndex = StrAdvanced.find("Телефон: ")
            ContactPersonIndex = StrAdvanced.find("Контактное лицо: ")
            EndIndex = StrAdvanced.find(" \nОтправить запрос")
            CountryIndex = StrAdvanced.find("Страна:\n")
            RegionIndex = StrAdvanced.find("Регион:\n")

            ArrName.append(StrAdvanced[NameIndex + 11:AdrrIndex].replace("\n", "") + " ")
            ArrAdrress.append(StrAdvanced[AdrrIndex:PhoneIndex].replace("\n", "") + " ")
            ArrPhone1.append(StrAdvanced[PhoneIndex:ContactPersonIndex].replace("\n", "") + " ")
            ArrContactPerson.append(StrAdvanced[ContactPersonIndex:EndIndex].replace("\n", "").replace("Контактное лицо:", "") + " ")
            ArrCountry.append(StrAdvanced[CountryIndex:RegionIndex].replace("\n", "").replace("Страна:", "") + " ")
            ArrRegion.append(StrAdvanced[RegionIndex:AdrrIndex].replace("\n", "").replace("Регион:", "") + " ")

            AlterF.write(StrAdvanced)

        else:  # если не подробный сайт
            StrNotAdvanced = ContactTableSoup.text
            # StrNotAdvanced = StrNotAdvanced.replace("Ваш E-mail:\nОтправить запрос\n\n\n", "")
            NameIndex = StrNotAdvanced.find("Название:\n")
            AdrrIndex = StrNotAdvanced.find("Адрес:\n")
            PhoneIndex = StrNotAdvanced.find("Телефон 1:\n")
            PhoneEndIndex = StrNotAdvanced.find("Ваш E-mail:\nОтправить запрос")
            ContactPersonIndex = StrNotAdvanced.find("Контактное лицо:\n")
            CountryIndex = StrNotAdvanced.find("Страна:\n")
            RegionIndex = StrNotAdvanced.find("Регион:\n")
            EndIndex = StrNotAdvanced.find("\n____")

            ArrName.append(StrNotAdvanced[NameIndex + 10:PhoneIndex].replace("\n", "") + " ")
            ArrPhone1.append(StrNotAdvanced[PhoneIndex:PhoneEndIndex].replace("\n", "") + " ")
            ArrAdrress.append(StrNotAdvanced[AdrrIndex:ContactPersonIndex].replace("\n", "") + " ")
            ArrContactPerson.append(StrNotAdvanced[ContactPersonIndex:EndIndex].replace("\n", "").replace("Контактное лицо:", "") + " ")
            ArrCountry.append(StrNotAdvanced[CountryIndex:RegionIndex].replace("\n", "").replace("Страна:", "") + " ")
            ArrRegion.append(StrNotAdvanced[RegionIndex:AdrrIndex].replace("\n", "").replace("Регион:", "") + " ")

            AlterF.write(StrNotAdvanced)

for i in range(len(ArrName)):
    print(ArrName[i])
    print(ArrCountry[i])
    print(ArrRegion[i])
    print(ArrAdrress[i])
    print(ArrPhone1[i])
    print(ArrContactPerson[i])
    i = i + 1
    print("______________________")

parsBD = pd.DataFrame(
    {'Название': CompanyName1, 'Название2': CompanyName2, 'Название3': ArrName, 'Сайт': CompanyLink1,
     'Сайт2': CompanyLink2, 'Страна': ArrCountry, 'Регион': ArrRegion, 'Адрес': ArrAdrress,
     'Телефон': ArrPhone1,
     'Контакты': CompanyPlaceMass, 'Контактное лицо': ArrContactPerson,
     'Описание': CompanyDescriptionMass})  # загрузка в эксель с помощью panda
parsBD.to_excel('./ParsResults.xlsx')
