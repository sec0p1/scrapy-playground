# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class CoinSpider(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = [
        'https://www.livecoin.net/en'
    ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        curr_dir = os.path.dirname(os.path.abspath(__file__))
        chrome_path = os.path.join(curr_dir, "./chromedriver")
        driver = webdriver.Chrome(
            executable_path=chrome_path,
            options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.livecoin.net/en")

        rur_tab = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        rur_tab[4].click()

        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        currencies = resp.xpath(
            '//div[contains(@class, "ReactVirtualized__Table__row ")]')
        for currency in currencies:
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
            }
