# Scrapy
## Scrapy components:
    - spiders
    - pipelines - piping actions on scraped data
    - middlewares - request / response, injecting custom headers, proxying
    - engine - ensures consistency between all operations that happen
    - scheduler - preserving the order of operations (FIFO)

## Spider classes:
    - scrapy.Spider
    - CrawlSpider
    - XMLFeedSpider
    - CSVFeedSpider
    - SitemapSpider

![](2020-02-19-11-07-53.png)

Engine is the connector for everything. When new request is added it is delegated from the engine to the scheduler queue, when it is in line for execution it is passed to the engine and then to the middleware which executes the request. Response is passed to the engine and then to the spider to handle the response and extract data. Extracted data is then sent to the ending which passes it to the pipeline to process the data.

