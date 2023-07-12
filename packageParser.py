import requests
import pandas as pd
from bs4 import BeautifulSoup

# https://www.youtube.com/watch?v=EF9UNlB05Rk&list=PL6plRXMq5RADYaw4Xo111smBcEPNMhdHf&index=3
# по другому гайду    https://idatica.com/blog/parsing-saytov-na-python-rukovodstvo-dlya-novichkov/  https://pishuverno.ru/kak-napisat-parser-dlya-sajta-na-python/
# Define URL

urlMain = "https://tara.unipack.ru"  # ссылка на отрасль
requests.get(urlMain)
MainPages = requests.get(urlMain)
# parser-lxml = Change html to Python friendly format
MainSoup = BeautifulSoup(MainPages.text, "lxml")  # код сайта готовый к обработки
MainFilteredParsRes = MainSoup.find("div",
                                    class_="content-work").find("ul")  # отфильтрованный код компаний

SphereLink1 = []
for elem in MainFilteredParsRes:
    Links = MainFilteredParsRes.find_all("a")
    for link in Links:
        link_url = link.get("href")
        link_text = link.text.strip()
        link_title = link.get("title")
        if link_title.find("Галерея продукции") == -1 and link_title.find("Публикации по теме") == -1:
            SphereLink1.append(link_url)
print("Собран массив сфер")

#SphereUrl = "https:" + SphereLink1[2]

def parsSphere(ParsUrl):
    SphereUrl = "https:" + ParsUrl
    requests.get(SphereUrl)
    pages = requests.get(SphereUrl)
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

    print("Собрана верхняя база по " + SphereUrl)
    # print (filteredParsRes)
    # with open ("resultParsing.txt", "w", encoding = "utf-8") as file:     file.write(str (filteredParsRes))
    # print(CompanyName1)
    # print(CompanyLink1)
    # print(CompanyPlaceMass)
    # print(CompanyDescriptionMass)
    ArrName = []
    ArrPhone1 = []
    ArrCountry = []
    ArrRegion = []
    ArrAdrress = []
    ArrContactPerson = []

    with open('AlternateResults.txt', "w") as AlterF:  # проход по всем страницам компаний
        for elem in CompanyLink1:  # проход по всем страницам компаний
            AlterF.write("________________________________________________________________________ \n")
            OneUrl = "https:" + elem + "/contacts"
            requests.get(OneUrl)
            pages = requests.get(OneUrl)
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
                ArrContactPerson.append(
                    StrAdvanced[ContactPersonIndex:EndIndex].replace("\n", "").replace("Контактное лицо:", "") + " ")
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
                ArrContactPerson.append(
                    StrNotAdvanced[ContactPersonIndex:EndIndex].replace("\n", "").replace("Контактное лицо:", "") + " ")
                ArrCountry.append(
                    StrNotAdvanced[CountryIndex:RegionIndex].replace("\n", "").replace("Страна:", "") + " ")
                ArrRegion.append(StrNotAdvanced[RegionIndex:AdrrIndex].replace("\n", "").replace("Регион:", "") + " ")

                AlterF.write(StrNotAdvanced)

    print("Собрана глубокая база по " + SphereUrl)
    # for i in range(len(ArrName)):
    #     print(ArrName[i])
    #     print(ArrCountry[i])
    #     print(ArrRegion[i])
    #     print(ArrAdrress[i])
    #     print(ArrPhone1[i])
    #     print(ArrContactPerson[i])
    #     i = i + 1
    #     print("______________________")

    parsBD = pd.DataFrame(
        {'Название': CompanyName1, 'Название2': CompanyName2, 'Название3': ArrName, 'Сайт': CompanyLink1,
         'Сайт2': CompanyLink2, 'Страна': ArrCountry, 'Регион': ArrRegion, 'Адрес': ArrAdrress,
         'Телефон': ArrPhone1,
         'Контакты': CompanyPlaceMass, 'Контактное лицо': ArrContactPerson,
         'Описание': CompanyDescriptionMass})  # загрузка в эксель с помощью panda
    parsBD.to_excel(
        './' + SphereUrl.replace("https://tara.unipack.ru/", "").replace("russia-", "") + 'ParsResults.xlsx')

    return 'Победа над ' + SphereUrl.replace("https://tara.unipack.ru/", "").replace("russia-", "")

#len(SphereLink1)
for i in range(2):
    ParsUrl = SphereLink1[i]
    a = parsSphere(ParsUrl)
    print(a)