import requests
from pprint import pprint
from lxml import html
from datetime import datetime, timedelta
from pymongo import MongoClient

day = datetime.today()
month = {1: ' Января ', 2: ' Февраля ', 3: ' Марта ', 4: ' Апреля ', 5: ' Мая ', 6: ' Июня ', 7: ' Июля ',
         8: ' Августа ', 9: 'Сентября ', 10: ' Октября ', 11: ' Ноября ', 12: ' Декабря '}

Articles = []


def fill_dict(dict, name, name_source, date, href):
    dict.append({'name': name, 'name source': name_source, 'date': date, 'link': href})


def parsing_lenta_a(dict, source):
    href = main_link[:-1] + source.xpath("./a/@href")[0]
    name = source.xpath(".//a/text()")[0].replace("\xa0", ' ')
    name_source = 'Lenta.ru'
    date = source.xpath(".//a/time/@title")[0] + ' в ' + source.xpath(".//a/time/text()")[0]
    fill_dict(dict, name, name_source, date, href)


def parsing_lenta_item_article(dict, source):
    if source[0].xpath(".//span[@class='g-date item__date']") == 'Сегодня':
        date = str(day.day) + month[day.month] + str(day.year) + ' в ' + source[0].xpath(
            ".//span[@class='time']").text_content()
    else:
        date = source[0].xpath(".//span[@class='g-date item__date']/text()")[0] + ' ' + str(day.year) + ' в ' + source[
            0].xpath(".//span[@class='time']/text()")[0]
    href = main_link[:-1] + source.xpath(".//div[@class='titles']/h3/a/@href")[0]
    name = source.xpath("./div[@class='titles']/h3/a/span/text()")[0].replace("\xa0", ' ')
    name_source = 'Lenta.ru'
    fill_dict(dict, name, name_source, date, href)


def parsing_lenta_item_news(dict, source):
    date = str(day.day) + month[day.month] + str(day.year) + ' в ' + source[0].xpath(
            ".//span[@class='time']")[0].text_content()
    href = main_link[:-1] + source.xpath(".//div[@class='titles']/h3/a/@href")[0]
    name = source.xpath("./div[@class='titles']/h3/a/span/text()")[0].replace("\xa0", ' ')
    name_source = 'Lenta.ru'
    fill_dict(dict, name, name_source, date, href)

main_link = 'https://yandex.ru/'
response = requests.get(main_link + 'news')
root = html.fromstring(response.text)

articles = root.xpath("//div[@class='story story_view_short story_notags']")

for article in articles:
    source_date = article.xpath(".//div[@class ='story__date']/text()")
    if '\xa0' in source_date[0]:
        source_date = source_date[0].replace("\xa0", ' ')
        date = str((day - timedelta(days=1)).day) + month[(day - timedelta(days=1)).month] + str(
            (day - timedelta(days=1)).year) + ' в ' + source_date[-5:]
        name_source = source_date[:-13]
    else:
        source_date = source_date[0]
        date = str(day.day) + month[day.month] + str(day.year) + ' в ' + source_date[-5:]
        name_source = source_date[:-5]
    name = article.xpath(".//div[@class ='story__topic']")[0].text_content()
    href = main_link[:-1] + article.xpath(".//div[@class='story__topic']/h2/a/@href")[0]
    fill_dict(Articles, name, name_source, date, href)

main_link = 'https://lenta.ru/'
response = requests.get(main_link)
root = html.fromstring(response.text)

root = root.xpath("//div[@class='span8 js-main__content']")
articles = root[0].xpath(".//div[@class='span4']")
source_first_item = articles[0].xpath(".//div[@class ='first-item']/h2")
parsing_lenta_a(Articles, source_first_item[0])

for article in articles:
    source_items = article.xpath(".//div[@class ='item']")
    for source_item in source_items:
        parsing_lenta_a(Articles, source_item)
    source_items = article.xpath(".//div[@class ='item article']")
    for source_item in source_items:
        parsing_lenta_item_article(Articles, source_item)
    source_items = article.xpath(".//div[@class ='item news b-tabloid__topic_news']")
    for source_item in source_items:
        parsing_lenta_item_news(Articles, source_item)

client = MongoClient('localhost', 27017)
db = client['users_db_280']
users = db.users280

users.insert_many(Articles)
