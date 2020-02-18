from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gderuparser.spiders.gderu import GderuSpider
from gderuparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(GderuSpider, mark='USB')
    process.start()
