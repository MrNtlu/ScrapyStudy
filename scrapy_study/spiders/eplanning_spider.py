# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class EplanningSpiderSpider(scrapy.Spider):
    name = 'eplanning_spider'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        urls = response.xpath("//a/@href").extract()
        for url in urls:
            if '#' == url:
                pass
            else:
                yield scrapy.Request(url=url,callback=self.parse_application)
            
    def parse_application(self,response):
        app_url= response.xpath("//*[@class='glyphicon glyphicon-inbox btn-lg']/following-sibling::a/@href").extract_first()
        yield scrapy.Request(url=response.urljoin(app_url),callback=self.parse_form)
    
    def parse_form(self, response):
        yield FormRequest.from_response(response, 
                                        formdata={'RdoTimeLimit': '42'}, 
                                        dont_filter=True, 
                                        formxpath='(//form)[2]', 
                                        callback=self.parse_pages)

    def parse_pages(self,response):
        # nextpage //li[@class='PagedList-skipToNext']//@href
        # pages //td/a/@href
        application_urls= response.xpath("//td/a/@href").extract()
        for url in application_urls:
            url=response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_items)
        
        next_page_url=response.xpath("//li[@class='PagedList-skipToNext']//@href").extract_first()
        absolute_next_page=response.urljoin(next_page_url)
        yield scrapy.Request(url=absolute_next_page, callback=self.parse_pages)

    def parse_items(self, response):
        agent_btn=response.xpath("//*[@value='Agents']/@style").extract_first()
        if 'display: inline;  visibility: visible;' in agent_btn:
            agent_name=response.xpath("//tr[th='Name :']/td/text()").extract_first()
            agent_address = response.xpath("//tr[th='Address :']/td/text()").extract_first()
            address_second = response.xpath("//tr[th='Address :']/following-sibling::tr//td/text()").extract()[0:3]
            for address in address_second:
                agent_address+=address
            agent_phone=response.xpath("//tr[th='Phone :']/td/text()").extract_first()
            agent_email=response.xpath("//tr[th='e-mail :']/td/a/text()").extract_first()
            yield{
                'Agent Name': agent_name,
                'Agent Address': agent_address,
                'Agent Phone': agent_phone,
                'Agent Email': agent_email,
                'url': response.url
            }
        else:
            self.logger.info('Agent button not found')

        
