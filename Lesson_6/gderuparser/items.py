# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

def return_photo(values):
    return values

def cleaner_price(value):
    return int(value[:-5].replace(' ', ''))

class GderuparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(return_photo))
    price = scrapy.Field(input_processor=MapCompose(cleaner_price), output_processor=TakeFirst())
    pass
