# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['http://www.superjob.ru/vacancy/search/?keywords=python&geo[c][0]=1']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css(
            'div._1ID8B div.f-test-vacancy-item a._1QIBo::attr(href)'
        ).extract()

        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        print(response)
        name = response.css('h1._3mfro.rFbjy.s1nFK._2JVkc::text').extract_first()
        salary = response.css('span._3mfro._2Wp8I.ZON4b.PlM3e._2JVkc span::text').extract()
        salary.extend((response.css('span._3mfro._2Wp8I.ZON4b.PlM3e._2JVkc::text').extract()[0], ))
        link = response.url
        site = self.allowed_domains[0]
        print(name, salary, response)
        yield JobparserItem(name=name, max_salary='', min_salary=salary, link=link, site=site)