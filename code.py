# pip install requests, BeautifulSoup4, lxml, pandas, matplotlib
import matplotlib.pyplot as plt
import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
from time import sleep
from Hidden import log_in, pass_in

url = "https://realt.by/rent/flat-for-long/bez-posrednikov/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0"
                  " Safari/537.36 Edg/109.0.1518.69",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9"
}

# ---Авторизация на сайте---

session = requests.Session()  # создаем Session объект
session.get("https://realt.by/rent/flat-for-long/bez-posrednikov/", headers=headers)  # заходим на сайт
url_log = "https://realt.by/login/?nextPage=https://realt.by/rent/flat-for-long/bez-posrednikov/"

session.get(url_log, headers=headers)

json_data = {
    'operationName': 'login',
    'query': 'mutation login($login: String!, $password: String!) {\n  login(login: $login, password: $password) '
             '{\n    ... on LoginResponse {\n      body {\n        token\n        agreementsNotAccepted\n      }\n    }'
             '\n    ...StatusAndErrors\n  }\n}\n\nfragment StatusAndErrors on INullResponse {\n  success\n  errors '
             '{\n    code\n    title\n    message\n    field\n  }\n}\n',
    'variables': {
        'login': log_in,
        'password': pass_in,
    },
}

result = session.post("https://realt.by/bff/graphql", json=json_data,
                      headers=headers)  # отправляем Post запрос на сайт, обратить внимание на ссылку!

# ---Проверяем, успешно ли была пройдена авторизация---

profile_info = "https://realt.by/account/profile/"
profile_response = session.get(profile_info, headers=headers).text
f = open("res_authorization.txt", "w", encoding="utf=8")  # сохраняем результат в текстовый файл
f.write(profile_response)
f.close()

# --- Работа с информацией на сайте---

response = session.get(url, headers=headers)
if response.status_code == 200:

    print(response.status_code)  # проверяем код состояния запроса страниц
else:
    print("Error!!!")

list_home = []  # создаем списки для записи полученной информации
a1 = []
a2 = []
a3 = []
a4 = []
price_list = []
list_all = []

page = int(input("Введите количество страниц для парсинга: "))

for num in range(0, page):

    sleep(1)  # Задержка отклика

    url = f"https://realt.by/rent/flat-for-long/bez-posrednikov/?page={num}"
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    f = open("html_page.txt", "w", encoding="utf=8")  # сохранить код страницы в файл для удобства
    f.write(str(soup))
    f.close()

    data = soup.find_all("div", class_="listing-item highlighted")  # находим все карточки квартир со страницы

    for item in data:  # запускаем цикл для получения интересующей информации
        price = item.find("div", class_="col-auto text-truncate").text.strip()
        price_num = ""
        for i in price:
            if i.isdigit():
                price_num += i
        price_list.append(price_num)
        list_all = [int(item) for item in price_list]
        for cv in list_all:
            if cv <= 800:
                a1.append(cv)
            elif 800 < cv <= 1000:
                a2.append(cv)

            elif 1001 < cv <= 1500:
                a3.append(cv)
            else:
                a4.append(cv)

        list_home.append(
            {
                "apart": item.find("a", class_="teaser-title").get("title"),
                "reference": item.find("a", class_="teaser-title").get("href"),
                "img_url": item.find("img", class_="lazy").get("data-original"),
                "info": item.find("div", class_="fs-small color-dark").find("p").find_next("p").text,
                "price_BYN": price_num

            }
        )
check_price = {
    "Квартиры до 800 р": len(a1),
    "Квартиры от 801 до 1000 р": len(a2),
    "Квартиры 1000 до 1500 р": len(a3),
    "Квартиры от 1501 р": len(a4),

}

# ---Cоздание графика---

graph = pd.Series(check_price)  # одномерный массив
plt.title("Круговая диаграмма  цен на квартиры в г. Минске", color="blue", fontstyle="oblique", fontsize=16,
          fontweight="bold")
plt.pie(graph, labels=graph.index, autopct="%1.1f%%", shadow=True, startangle=190)
# plt.title("График  цен на квартиры в г. Минске")   #  (2-й вариант графика)
# plt.bar(graph.index, height=graph)
plt.show()

# ---Запись в файл с помощью Pandas---

df = pd.DataFrame(list_home)
# print(df)
df.to_csv("Table_df.csv", sep=";")

# ---Записываем информацию в csv-файл---

sfile = "table.csv"

with open(sfile, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Name", "Link", "Photo", "Info", "Price_BYN"])

    for i in list_home:
        writer.writerow([i["apart"], i["reference"], i["img_url"], i["info"], i["price_BYN"]])
