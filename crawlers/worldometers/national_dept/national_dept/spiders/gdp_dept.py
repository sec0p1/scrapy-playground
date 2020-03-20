# -*- coding: utf-8 -*-
import scrapy


class GdpDeptSpider(scrapy.Spider):
    name = 'gdp_dept'
    allowed_domains = ['http://worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt']

    def parse(self, response):
        country_rows = response.xpath(
            '//table[@class="datatableStyles__StyledTable-bwtkle-1 hOnuWY table table-striped"]/tbody/tr')
        for row in country_rows:
            country_name = row.xpath('(.//td)[1]/a/text()').get()
            dept = row.xpath('(.//td)[2]/text()').get()
            yield {
                'country_name': country_name,
                'national_dept': dept
            }
