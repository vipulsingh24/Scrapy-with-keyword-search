# -*- coding: utf-8 -*-
import scrapy
from datetime import timedelta, date
import datetime

class MyItem(scrapy.Item):
	Title = scrapy.Field()
	Date = scrapy.Field()
	Article = scrapy.Field()
	url = scrapy.Field()

def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days)):
		yield start_date + timedelta(n)

class ThehinduSpider(scrapy.Spider):
	name = 'thehindu'
	allowed_domains = ['thehindu.com']
	start_urls = ['http://www.thehindu.com/archive/']
	keyword = input("Enter the keyword to be scrape: ")

	def start_requests(self):
		
		prev_day = (date.today()).strftime('%d/%m/%Y')
		max_date = datetime.datetime.strptime(prev_day, '%d/%m/%Y')
		min_date = datetime.datetime.strptime('1/1/2000', '%d/%m/%Y')

		while True:
			try:
				start_date = datetime.datetime.strptime(input('Enter start date (dd/mm/yyyy): '), '%d/%m/%Y')
				if (start_date < min_date or start_date > max_date):
					print('Enter the date from 1/1/2000 till today')
					continue
				else:
					break
			except ValueError:
				print('Invalid Date')
		
		while True:
			try:
				end_date = datetime.datetime.strptime(input('Enter end date (dd/mm/yyyy): '), '%d/%m/%Y')
				if (end_date < min_date or end_date > max_date):
					print('Enter the date from 1/1/2000 till today')
				elif ( end_date < start_date):
					print("End date can't be less than start date")
					continue				
				else:
					break
			except ValueError:
				print('Invalid Date')

		urls = ['http://www.thehindu.com/archive/web/', 'http://www.thehindu.com/archive/print/']
	
		for single_date in daterange(start_date, end_date):
			if ( single_date < datetime.datetime.strptime('1/1/2006', '%d/%m/%Y') ):
				yield scrapy.Request(url = "http://www.thehindu.com/thehindu/"+single_date.strftime('%Y/%m/%d')+"/99hdline.htm", callback=self.parse_day)
			else:
				if ( single_date < datetime.datetime.strptime('15/8/2009', '%d/%m/%Y') ):
					yield scrapy.Request(url = "http://www.thehindu.com/archive/print/"+single_date.strftime('%Y/%m/%d')+"/", callback=self.parse_day)
				else:						
					for url in urls:
						yield scrapy.Request(url = url+single_date.strftime('%Y/%m/%d')+"/", callback=self.parse_day)


	def parse_day(self, response):
		sel_article = response.xpath('//li/a[contains(text(), "'+self.keyword+'")]/@href').extract()
		for link in sel_article:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_article)

# http://www.thehindu.com/thehindu/2004/09/16/

# sel_article = response.xpath('//span/a[contains(text(), "'+self.keyword+'")]/@href')

# Article

# Date 1/1/2000-30/11/2001
# response.xpath('//td/font[2]/text()').extract_first()
# response.xpath('//center/font[2]/text()').extract_first()
# response.xpath('//td/font[2]/text()').extract_first()

# Headline
# response.xpath('//h3/font/text()').extract_first()
# response.xpath('//font[@class="storyhead"]/b/text()').extract_first()


# Article content
# response.xpath('//p/text()').extract() 
# response.xpath('//p/text()').extract() 

# date from 1/1/2006 - today
# response.xpath('//div[2]/div/span/none/text()').extract()
# Headline
# response.xpath('//div/h1/text()').extract()
# Article content
# response.xpath('//p/text() | //p/b/text() | //p/i/text()').extract()

	def parse_article(self, response):
		item = MyItem()
		item['Date'] = response.xpath('//td/font[2]/text() | //center/font[2]/text() | //div[2]/div/span/none/text()').extract_first()
		item['Title'] = response.xpath('//h3/font/text() | //font[@class="storyhead"]/b/text() | //div/h1/text()').extract_first()
		item['Article'] = response.xpath('//p/text() | //p/b/text() | //p/i/text()').extract()
		item['url'] = response.url
		yield item
