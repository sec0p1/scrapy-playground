import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from bookstoscrape.spiders.all_books import AllBooksSpider


process = CrawlerProcess(settings=get_project_settings())
process.crawl(AllBooksSpider)
process.start()
