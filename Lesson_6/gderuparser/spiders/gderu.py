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
        ads_links = response.xpath('//li[@class=""]//div[@class="title"]/a/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=GderuparserItem(), response=response)
        loader.add_css('name', 'h1.product-name::text')
        loader.add_xpath('price', '//div[@class="control-holder"]//span[@class="price"]/text()')
        loader.add_xpath('photos', '//li[@class="slide-item"]//img/@src')
        yield loader.load_item()
        # name = response.css('h1.title-info-title span.title-info-title-text::text').extract_first()
#         # photos = response.xpath('//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
#         # price = response.xpath('//span[@class="js-item-price"][1]/text()').extract_first()
#         # yield GderuparserItem(name=name, photos = photos, price = price)
#         # print(name, photos, price)


