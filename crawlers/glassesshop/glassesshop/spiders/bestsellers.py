# -*- coding: utf-8 -*-
import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        products = response.xpath(
            "//div[@class='col-sm-6 col-md-4 m-p-product']")

        # Handle products on a page:
        for product in products:
            product_name = product.xpath(".//div[@class='row']/p/a/text()").get()
            product_link = product.xpath(".//div[@class='pimg default-image-front']/a/@href").get()
            product_image = product.xpath(".//div[@class='pimg default-image-front']/a/img/@src").get()

            special_price = product.xpath(".//div[@class='row']/div[@class='pprice col-sm-12']/span/span/text()").get()
            if special_price:
                product_price = special_price
            else:
                product_price = product.xpath(".//div[@class='row']/div[@class='pprice col-sm-12']/span/text()").get()

            if product_name:
                yield {
                    "product_name": product_name,
                    "product_price": product_price,
                    "product_link": product_link,
                    "product_image": product_image
                }

        # Handle pagination:
        next_link = response.xpath("//a[@class='page-link' and @rel='next']/@href").get()
        print(next_link)
        if next_link:
            yield scrapy.Request(url=next_link, callback=self.parse)
