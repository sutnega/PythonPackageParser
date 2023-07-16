import requests
import pandas as pd
from bs4 import BeautifulSoup

# https://www.youtube.com/watch?v=EF9UNlB05Rk&list=PL6plRXMq5RADYaw4Xo111smBcEPNMhdHf&index=3
# по другому гайду    https://idatica.com/blog/parsing-saytov-na-python-rukovodstvo-dlya-novichkov/  https://pishuverno.ru/kak-napisat-parser-dlya-sajta-na-python/
# Define URL
PARSVAR = 1  # 1 сохранять сферы в отдельные файлы     2 сохранить все в один файл
PARSNUM = 1  # 1 спарсить первые PARSCOUNT сфер        2 спарсить все
PARSCOUNT = 20
STARTNUM = 0
# https://tara.unipack.ru/russia 42
# https://material.unipack.ru/russia 20
# https://propack.unipack.ru/russia
# https://packmash.unipack.ru/russia  23
# https://foodmash.unipack.ru/russia 21
# https://brand.unipack.ru/russia 30
#https://plasmash.unipack.ru/russia 36
#https://log.unipack.ru/russia 8
#https://print.unipack.ru/russia 6
#https://service.unipack.ru/russia 55
#https://nonfood.unipack.ru/russia 28
urlMain = "https://material.unipack.ru/russia"  # ссылка на отрасль
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
        if link_title.find("Галерея продукции") == -1 and link_title.find("Публикации по теме") and link_title.find(
                "Цены на продукцию") == -1:
            SphereLink1.append(link_url)
print("Собран массив сфер")


# 1 сохранять в отдельные файлы  2 выдать DataFrame pandas
def parsSphere(ParsUrl, ParsMode):
    SphereUrl = "https:" + ParsUrl
    pages = requests.get(SphereUrl)
    # parser-lxml = Change html to Python friendly format
    soup = BeautifulSoup(pages.text, "lxml")  # код сайта готовый к обработки
    filteredParsRes = soup.find_all("div",
                                    class_="product-section")  # product-section simple,   отфильтрованный код компаний

    MorePages = soup.find("ul", class_="page-nav mt30")  # проверка на наличие вложенных страниц
    SphereName = soup.find("div", class_="js-select-region")
    print(SphereName.text)
    if MorePages != None:
        IsMorePages = MorePages.find_all("a")  # product-section simple,   отфильтрованный код компаний
        PagesNum = IsMorePages[-1].text
        print("страниц: "+PagesNum)
        for i in range(int(PagesNum)):
            print(f"?page={i}")

    # верхний парсинг страницы
    with open('filteredParsResults.txt', "w") as f:
        CompanyName1 = []
        CompanyName2 = []
        CompanyLink1 = []
        CompanyLink2 = []
        CompanyPlaceMass = []
        CompanyDescriptionMass = []

        def topParser(filteredParsRes):
            for elem in filteredParsRes:
                Links = elem.find_all("a")
                #print(Links)
                if Links==None: print ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
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
                        if link_url.find("/about_one/3/#3 ") == -1 :CompanyLink1.append(link_url)
                        else: CompanyLink1.append(" ")
                    if link == Links[-1] and link_url.find("/about_one/3/#3") == -1 : CompanyLink2.append(link_url + " ")
                    else:
                        if link==Links[-1] and link_url.find("/about_one/3/#3")!=-1:CompanyLink2.append(" broken ")

                f.write(f"Место: {CompanyPlace.text}\n")
                f.write(f"Описание: {CompanyDescription.text}\n")
                CompanyPlaceMass.append(CompanyPlace.text + " ")
                CompanyDescriptionMass.append(CompanyDescription.text + " ")

            return CompanyLink1


        if MorePages != None:
            for i in range(int(PagesNum)):
                MoreSphereUrl = SphereUrl + "?page=" + str(i)
                Mpages = requests.get(MoreSphereUrl)
                # parser-lxml = Change html to Python friendly format
                Msoup = BeautifulSoup(Mpages.text, "lxml")  # код сайта готовый к обработки
                MfilteredParsRes = Msoup.find_all("div",
                                                  class_="product-section")  # product-section simple,   отфильтрованный код компаний
                test = topParser(MfilteredParsRes)
                print(test)
                print(CompanyName1)
        else:
            test = topParser(filteredParsRes)

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
    # глубокий парсинг компаний
    with open('AlternateResults.txt', "w") as AlterF:  # проход по всем страницам компаний

        for i in range(len(CompanyLink2)):
            if i< len(CompanyLink2)-2:
                if  CompanyLink2[i] == " broken " and CompanyLink2[i + 1] == " broken " :
                    CompanyLink2 = CompanyLink2[0:i] + CompanyLink2[i+2:]

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

    print(f"ArrAdrress =   {ArrAdrress}")
    print(f"ArrContactPerson =   {ArrContactPerson}")
    print(f"ArrCountry =   {ArrCountry}")
    print(f"ArrName =  {ArrName}")
    print(f"ArrPhone1 =   {ArrPhone1}")
    print(f"ArrRegion =   {ArrRegion}")
    print(f"CompanyDescriptionMass =   {CompanyDescriptionMass}")
    print(f"CompanyLink1 =   {CompanyLink1}")
    print(f"CompanyName1 =   {CompanyName1}")
    print(f"CompanyName2 =   {CompanyName2}")
    print(f"CompanyLink2 =   {CompanyLink2}")
    print(f"CompanyPlaceMass =   {CompanyPlaceMass}")

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

    if ParsMode == 1:
        parsBD.to_excel('ParsResult_' + SphereName.text.replace('/', "").replace('\\', "").replace(':', "") + ".xlsx")
        # parsBD.to_excel('ParsResult_' + "test" + ".xlsx")
        # 'ParsResult_' + SphereUrl.replace(urlMain + "/", "").replace("russia-", "") + ".xlsx")

        return 'Победа над ' + SphereUrl.replace(urlMain + "/", "").replace("russia-", "")
    else:
        if ParsMode == 2: return parsBD


Mass = SphereLink1[STARTNUM:PARSCOUNT]
fixNum = 0
fixElem = 0

if fixNum == 0:
    if PARSNUM == 1:
        ParsingVar = PARSCOUNT
    else:
        if PARSNUM == 2: ParsingVar = len(SphereLink1)
    if PARSVAR == 2:
        writer = pd.ExcelWriter('./FullBD.xlsx', engine='xlsxwriter')
        BD_sheets = {}
        # len(SphereLink1)
        for i in range(ParsingVar):  # строка для запуска парсера  вставить строку свыше
            ParsUrl = Mass[i]
            a = parsSphere(ParsUrl, 2)
            BD_sheets[str(i + 1) + ' '] = a
        for sheet_name in BD_sheets.keys():
            BD_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
        writer.close()
    else:
        for i in range(ParsingVar):
            ParsUrl = Mass[i]
            a = parsSphere(ParsUrl, 1)
            print(a)
            b = i + STARTNUM
            print("Сохранен файл номер ")
            print(b)
else:
    if fixNum == 1:
        ParsUrl = SphereLink1[fixElem]
        a = parsSphere(ParsUrl, 1)
        print()

print(SphereLink1)