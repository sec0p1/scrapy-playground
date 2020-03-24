# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AllBooksSpider(CrawlSpider):
    name = 'all_books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//div[@class='image_container']/a"),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(restrict_xpaths="//li[@class='next']/a")
        )
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            'price': response.xpath("//div[@class='col-sm-6 product_main']/p[@class='price_color']/text()").get()
        }
