# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    url = "http://quotes.toscrape.com"

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))

            splash:set_viewport_full()

            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url=self.url + '/js',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        quotes = response.xpath(
            '//div[@class="quote"]'
        )
        for quote in quotes:
            yield {
                'text': quote.xpath('.//span[1]/text()').get(),
                'author': quote.xpath('.//span[2]/small/text()').get(),
                'tags': quote.xpath('.//div[@class="tags"]/a/text()').getall()
            }

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            next_page = response.urljoin(next_link)
            yield SplashRequest(
                url=next_page,
                callback=self.parse,
                endpoint='execute',
                args={
                    'lua_source': self.script
                }
            )
