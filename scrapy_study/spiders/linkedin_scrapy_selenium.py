# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from parsel import Selector
from time import sleep
from selenium.webdriver.common.keys import Keys
import csv

def validate_field(field):
    if field:
        pass
    else:
        field=''
    return field

file_name='results_file.csv'
linkedin_email='email@gmail.com'
linkedin_password='password'

writer=csv.writer(open(file_name,'w+'))
writer.writerow(['Name', 'Job Title', 'School', 'Location', 'Url'])

driver=webdriver.Chrome('/Users/burak/Desktop/chromedriver')
driver.get('https://www.linkedin.com')
username= driver.find_element_by_class_name('login-email')
username.send_keys(linkedin_email)
sleep(0.5)

password= driver.find_element_by_id('login-password')
password.send_keys(linkedin_password)
sleep(0.5)
login_button = driver.find_element_by_xpath("//*[@type='submit']")
login_button.click()
sleep(5)

driver.get('https://www.google.com')
sleep(3)

search_query=driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "python developer" AND "London"')
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

linkedin_urls=driver.find_elements_by_tag_name('cite')
linkedin_urls=[url.text for url in linkedin_urls]
sleep(0.5)

for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(5)

    sel=Selector(text=driver.page_source)
    name= sel.xpath('//h1/text()').extract_first()
    title= sel.xpath('//h2/text()').extract_first()
    school=sel.xpath("//span[@class='pv-top-card-v2-section__entity-name pv-top-card-v2-section__school-name text-align-left ml2 t-14 t-black t-bold lt-line-clamp lt-line-clamp--multi-line ember-view']/text()[2]").extract_first()
    if school:
        school=school.strip()
    location=sel.xpath("//h3[@class='pv-top-card-section__location t-16 t-black--light t-normal mt1 inline-block']/text()[2]").extract_first()
    if location:
        location=location.strip()
    linkedin_url=driver.current_url

    name=validate_field(name)
    title=validate_field(title)
    school=validate_field(school)
    location=validate_field(location)
    linkedin_url=validate_field(linkedin_url)

    print('/n')
    print('Name: '+ name)
    print('Job Title: '+ title)
    print('School: '+ school)
    print('Location: '+ location)
    print('Url: '+ linkedin_url)

    writer.writerow([name,
                    title,
                    school,
                    location,
                    linkedin_url])
    
    try: 
        connect_button=driver.find_element_by_xpath("//span[text()='Connect']")
        connect_button.click()
        sleep(3)

        send_request=driver.find_element_by_xpath("//button[@class='button-primary-large ml1']")
        send_request.click()
        sleep(3)
    except:
        pass

    
driver.quit()

# class LinkedinScrapySpider(scrapy.Spider):
#     name = 'linkedin_scrapy'
#     allowed_domains = ['linkedin.com']
#     start_urls = ['https://www.linkedin.com']

#     def parse(self, response):
#         pass
