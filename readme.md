# **Парсинг сайта с авторизацией и визуализацией данных!** 
___
![Python](https://img.shields.io/pypi/pyversions/pip?color=g)
![stars](https://img.shields.io/redmine/plugin/stars/redmine_xlsx_format_issue_exporter?color=blueviolet)
![quality](https://img.shields.io/ansible/quality/432?color=yellow)
## Pip install:
>pip install requests, BeautifulSoup4, lxml, pandas, matplotlib
## Описание:

## `ВАЖНО:no_entry:`
:white_check_mark:Данный проект был написан непосредственно для сайта квартир: https://realt.by/rent/flat-for-long/bez-posrednikov/. В проекте
реализована идея сбора определенных данных с вышеуказанного сайта.

```python
    url = f"https://realt.by/rent/flat-for-long/bez-posrednikov/?page={num}"
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

```

:white_check_mark:Данные извлекаются из HTML-кода страниц и записываются в файл в формате "csv".

:white_check_mark:Также код данной программы предусматривает авторизацию пользователя на сайте.Чтобы использовать свои данные на авторизацию внесите их в код в файле Нidden.py
>>>Не передавайте свои личные данные третьим лицам!
```python
log_in = "***********@gmail.com"
pass_in = "*********"
```

:diamonds: Информация по цене квартир представляется в виде круговой диаграммы, где категории диаграммы указаны в процентном соотношении.

:cyclone:Документация:

+ [Matplotlib](https://matplotlib.org/stable/tutorials/introductory/pyplot.html) 

+ [Pandas](https://pandas.pydata.org/docs/)

+ [BeautifulSoup](https://pypi.org/project/BeautifulSoup/)

+ [Requests](https://pypi.org/project/requests/)
