# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from gderuparser.items import GderuparserItem
from scrapy.loader import ItemLoader


class GderuSpider(scrapy.Spider):
    name = 'gderu'
    allowed_domains = ['gde.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://gde.ru/yelektronnaya_tehnika?Filter[district_id]=&Filter[search_string]={mark}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//li[@class="text control forward last-none"]/a/@href').extract_first()
        ads_links = response.xpath('//li[@class=""]//div[@class="title"]/a/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=GderuparserItem(), response=response)
        loader.add_css('name', 'h1.product-name::text')
        loader.add_xpath('price', '//div[@class="control-holder"]//span[@class="price"]/text()')
        loader.add_xpath('photos', '//li[@class="slide-item"]//img/@src')
        yield loader.load_item()


