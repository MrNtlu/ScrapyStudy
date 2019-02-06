# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BooksCrawlerSpider(CrawlSpider):
    name = 'books_crawler'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        Rule(LinkExtractor(deny=('Books'),restrict_xpaths="//ul[@class='nav nav-list']//ul/li/a"), callback='parse_item',follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for book in response.xpath("//div/ol[@class='row']//li/*[@class='product_pod']"):
            book_url=response.request.url
            # Meta sends this value to next one
            yield scrapy.Request(url=response.urljoin(book.xpath("./h3/a/@href").extract_first()), callback=self.parse_book,meta={'url':book_url})

        
    def parse_book(self, response):
        yield{
            'description':response.xpath("//*[@class='product_page']/p/text()").extract_first(),
            'title':response.xpath("//*[@class='col-sm-6 product_main']/h1/text()").extract_first(),
            'url':response.meta['url']
        }
        