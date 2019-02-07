import scrapy


class ClassCentralSpider(scrapy.Spider):
    name = 'class_central'
    start_urls = ['https://www.class-central.com/subjects']

    def parse(self, response):
        for row in response.xpath("//*[@class='width-100 medium-up-width-1-2 xlarge-up-width-1-3 col margin-vert-medium medium-up-margin-vert-xlarge medium-up-padding-right-large xlarge-up-padding-right-xlarge']"):
            title=row.xpath(".//*[@class='head-3 large-up-head-2 text--bold block']/text()").extract_first()
            # Get certain title ex: Computer Science
            # title=row.xpath(".//*[@class='head-3 large-up-head-2 text--bold block'][contains(text(),'Computer Science')]/text()").extract_first()
            subjects=row.xpath(".//li/a/text()").extract()
            urls=row.xpath(".//li/a/@href").extract()
            for i in range(len(urls)):
                url=urls[i]
                subject=subjects[i]
                yield scrapy.Request(url=response.urljoin(url),callback=self.parse_subject, meta={'title': title, 'subject':subject})
                

    def parse_subject(self, response):
        title=response.meta['title']
        subject=response.meta['subject']
        for courses in response.xpath("//tbody[@class='table-body-subjectstable']//td[2]"):
            description=courses.xpath(".//*[@itemprop='name']/text()").extract_first()
            course_url=courses.xpath("./a[1]/@href").extract_first()
            yield scrapy.Request(url=response.urljoin(course_url),callback=self.parse_course, meta={'title': title, 'subject':subject,'description':description})

    
    def parse_course(self, response):
        title=response.meta['title']
        subject=response.meta['subject']
        description=response.meta['description']
        course_description=''
        course_descriptions=response.xpath("//div[@class='relative fade-bottom fade-hidden']/text()").extract()
        for desc in course_descriptions:
            course_description=course_description+desc

        course_info=response.xpath("//*[@class='col push width-100 large-up-width-2-5 xlarge-up-width-1-3 large-up-padding-left-small margin-top-xsmall']//ul/li/span[@class='text-2 text--charcoal width-2-3 block col']/text()|//*[@class='col push width-100 large-up-width-2-5 xlarge-up-width-1-3 large-up-padding-left-small margin-top-xsmall']//ul/li/a[not(contains(text(),'Learn more about MOOCs'))]/text()").extract()
        course_titles=response.xpath("//*[@class='col push width-100 large-up-width-2-5 xlarge-up-width-1-3 large-up-padding-left-small margin-top-xsmall']//ul/li/strong[not(contains(text(),'Start Date'))]/text()").extract()
        course_dict=dict()
        for i in range(len(course_info)):
            course_dict[course_titles[i].strip()]=course_info[i].strip()
        # provider=course_info[0].strip()
        # course_subject=course_info[1].strip()
        # course_cost=course_info[2].strip()
        # course_session=course_info[3].strip()
        # course_language=course_info[4].strip()
        # course_effort=course_info[6].strip()
        # course_duration=course_info[7].strip()

        yield{
            'title':title,
            'subject': subject.strip(),
            'description': description.strip(),
            'course_desc': course_description.strip(),
            'course_info':course_dict
        }

            