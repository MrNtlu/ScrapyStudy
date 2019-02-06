# -*- coding: utf-8 -*-
import scrapy
import os
import glob

class BookSpiderSpider(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['books.toscrape.com/']
    start_urls = ['http://books.toscrape.com/']

    def __init__(self, category): # Scrapy with arguments (gets argument with -a)
        self.start_urls=[category]

    def start_requests(self):
        #url='http://books.toscrape.com/'
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        for book in response.xpath("//div/ol[@class='row']//li/*[@class='product_pod']"):
            yield{
                'book_title': book.xpath("./h3/a/text()").extract_first(),
                'price': book.xpath("./div[@class='product_price']/p[@class='price_color']/text()").extract_first(),
                'link': response.request.url
            }

        next_page=response.xpath("//li[@class='next']/a/@href").extract_first()

        if next_page is not None:
            next_page_link=response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link,callback=self.parse)

    def close(self, reason): # Handles on close
        csv_file=max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file,'result.csv')