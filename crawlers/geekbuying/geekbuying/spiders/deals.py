# -*- coding: utf-8 -*-
import scrapy


class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['www.geekbuying.com']
    start_urls = ['https://www.geekbuying.com/deals/categorydeals']

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.geekbuying.com/deals/categorydeals',
            callback=self.parse,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
            })

    def parse(self, response):
        products = response.xpath("//div[@class='flash_li']")

        for product in products:
            product_name = product.xpath('.//a[2]/text()').get()
            product_link = product.xpath(".//a[1]/@href").get()
            product_price = product.xpath(
                ".//div[@class='flash_li_price']/span/text()").get()

            yield {
                "product_name": product_name,
                "product_link": product_link,
                "product_price": product_price,
                "User-Agent": response.request.headers['User-Agent'].decode()
            }

        next_page = response.xpath("//a[@class='next']/@href").get()
        if next_page:
            yield response.follow(
                url=next_page,
                callback=self.parse,
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
                })
