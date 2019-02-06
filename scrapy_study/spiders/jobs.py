# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr']

    def parse(self, response):
        for job in response.xpath("//ul[@class='rows']/li[@class='result-row']"):
            title=job.xpath(".//p[@class='result-info']/a/text()").extract_first()
            url=job.xpath("./a/@href").extract_first()
            yield scrapy.Request(url=url, callback=self.parse_job, meta={'title': title,
                                                                        'url': url })
        
        next_page=response.xpath("//*[@class='button next']/@href").extract_first()

        if next_page is not None:
            next_page_link=response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_job(self, response):
        descriptions= response.xpath("//*[@id='postingbody']/text()").extract()
        title= response.meta['title']
        url= response.meta['url']
        compensation=response.xpath("//*[@class='attrgroup']/span[1]/b/text()").extract_first()
        employment_type=response.xpath("//*[@class='attrgroup']/span[2]/b/text()").extract_first()
        address=response.xpath("//div[@class='mapaddress']/text()").extract_first()
        description_clear=''
        for description in descriptions:
            description_clear=description_clear+description.strip()
        if address is None:
            address="Unknown"
        yield{
            'title': title,
            'url': url,
            'description': description_clear,
            'compensation': compensation,
            'employment_type': employment_type,
            'address': address
        }