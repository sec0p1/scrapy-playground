# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating',
            headers={
                'User-Agent': self.user_agent
            }
        )

    # Rule order is important.
    # If we first used next page rule, page would be swithced without movies being crawled
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"),
            callback='parse_item',
            follow=True,
            process_request='set_user_agent'
        ),
        Rule(
            LinkExtractor(restrict_xpaths="//a[@class='lister-page-next next-page'][1]"),
            process_request='set_user_agent'
        )
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
            'year': response.xpath("//span[@id='titleYear']/a/text()").get(),
            'duration': response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(),
            'genre': response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            'rating': response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'movie_url': response.url,
            'User-Agent': response.request.headers['User-Agent'].decode()
        }
