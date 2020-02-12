# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongobase = client.vacansy_280

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            if len(item['min_salary']) == 1:
                item['max_salary'] = None
                min_salary = item['min_salary'][0].replace("\xa0", '')
                if min_salary.find('от') == 0:
                    if min_salary.find('до') != -1:
                        item['max_salary'] = int(min_salary[min_salary.find('до')+3:min_salary.find('руб')])
                        item['min_salary'] = int(min_salary[3:min_salary.find('до')])
                    else:
                        item['min_salary'] = int(min_salary[3:min_salary.find('руб')])
                else:
                    item['min_salary'] = None
            elif len(item['min_salary']) == 5:
                item['max_salary'] = None
                item['min_salary'] = int(item['min_salary'][1].replace("\xa0", ''))
            elif len(item['min_salary']) == 7:
                item['max_salary'] = int(item['min_salary'][3].replace("\xa0", ''))
                item['min_salary'] = int(item['min_salary'][1].replace("\xa0", ''))
        elif spider.name == 'superjob':
            min_salary = item['min_salary']
            if len(min_salary) == 3:
                if min_salary[-1] == 'от' or min_salary[-1] == '\xa0':
                    item['min_salary'] = int(min_salary[0].replace("\xa0", ''))
                    item['max_salary'] = None
                if min_salary[-1] == 'до':
                    item['max_salary'] = int(min_salary[0].replace("\xa0", ''))
                    item['min_salary'] = None
            elif len(min_salary) == 7:
                item['max_salary'] = int(min_salary[4].replace("\xa0", ''))
                item['min_salary'] = int(min_salary[0].replace("\xa0", ''))
            else:
                item['max_salary'] = None
                item['min_salary'] = None

        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        print(item['min_salary'])

        return item
