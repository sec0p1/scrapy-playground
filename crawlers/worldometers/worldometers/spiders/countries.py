# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['http://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            # . is becouse we do not use response
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = f"https://www.worldometers.info{link}"
            # more fancy way:
            absolute_url = response.urljoin(link)

            # if we want to use just the relative url:
            # yield response.follow(url=link)

            # meta is used to pass the data between parse mathods
            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse_country,
                meta={'country_name': name})

    def parse_country(self, response):
        rows = response.xpath(
            '(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')

        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'country_name': response.request.meta['country_name'],
                'year': year,
                'population': population
            }
