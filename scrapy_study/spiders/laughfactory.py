# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy_study.items import ScrapyStudyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LaughfactorySpider(CrawlSpider):
    name = 'laughfactory'
    allowed_domains=['laughfactory.com']
    start_urls = ['http://www.laughfactory.com/jokes']
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='jokes-nav']//li/a"), callback='parse_item',follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), callback='parse_item', follow=True),
    )
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        for joke in response.xpath("//div[@class='jokes']"):
            #With Yield
            yield {
                'joke': joke.xpath(".//p/text()").extract_first().strip(),
                'likes': joke.xpath(".//a[@class='like']/span/text()").extract_first(),
                'dislikes': joke.xpath(".//a[@class='dislike']/span/text()").extract_first(),
                'title': response.xpath("//h1/span[2]/text()").extract_first().strip(),
                'link': response.request.url
            }

            # With Item Class
            # loader= ItemLoader(item=ScrapyStudyItem(), selector=joke, response=response) 
            # loader.add_xpath('joke',".//p/text()")
            # loader.add_xpath('likes',".//a[@class='like']/span/text()")
            # loader.add_xpath('dislikes',".//a[@class='dislike']/span/text()")
            # yield loader.load_item()

        # next_page=response.xpath("//li[@class='next']/a/@href").extract_first()

        # if next_page is not None:
        #     next_page_link= response.urljoin(next_page)
        #     yield scrapy.Request(url= next_page_link, callback= self.parse)