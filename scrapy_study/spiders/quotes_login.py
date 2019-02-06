# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class QuotesLoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        csrf_token=response.xpath("//*[@name='csrf_token']/@value").extract_first()
        yield scrapy.FormRequest(self.start_urls[0],
            formdata={
                'csrf_token': csrf_token,
                'username': 'foobar',
                'password': 'foobar'
                },callback=self.parse_after_login)

    def parse_after_login(self,response):
        #open_in_browser(response)
        if response.request.url == self.start_urls[0]:
            yield scrapy.Request(url= "http://quotes.toscrape.com/", callback= self.parse_after_login)
        else:
            yield{
                'response': response,
                'response_url': response.request.url,
                'login/logout': response.xpath("//div[@class='col-md-4']/p/a/text()").extract_first()
            }