# -*- coding: utf-8 -*-
import scrapy
from datetime import timedelta, date
import datetime

class MyItem(scrapy.Item):
	Title = scrapy.Field()
	Date = scrapy.Field()
	article = scrapy.Field()

def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days)):
		yield start_date + timedelta(n)

class ThehinduSpider(scrapy.Spider):
	name = 'thehindu'
	allowed_domains = ['thehindu.com']
	start_urls = ['http://www.thehindu.com/archive/']
	keyword = input("Enter the keyword to be scrape: ")

	def start_requests(self):
		
		prev_day = (date.today()-timedelta(1)).strftime('%d/%m/%Y')
		max_date = datetime.datetime.strptime(prev_day, '%d/%m/%Y').date()	
		min_date = datetime.datetime.strptime('1/1/2000', '%d/%m/%Y')

		while True:
			try:
				start_date = datetime.datetime.strptime(input('Enter start date (dd/mm/yyyy): '), '%d/%m/%Y')
				if (start_date < min_date or start_date > max_date):
					print('Enter the date from 1/1/2000 till yesterday')
					continue
				else:
					break
			except ValueError:
				print('Invalid Date')
		
		while True:
			try:
				end_date = datetime.datetime.strptime(input('Enter end date (dd/mm/yyyy): '), '%d/%m/%Y')
				if (end_date < min_date or end_date > max_date):
					print('Enter the date from 1/1/2000 till yesterday')
				elif ( end_date < start_date):
					print("End date can't be less than start date")
					continue				
				else:
					break
			except ValueError:
				print('Invalid Date')
			
		
		for single_date in daterange(start_date, end_date):
			if ( single_date < datetime.datetime.strptime('1/1/2006', '%d/%m/%Y') ):
				yield scrapy.Request(url = "http://www.thehindu.com/thehindu/"+single_date.strftime('%Y/%m/%d')+"/99hdline.htm", callback=self.parse_day_old)
			else:
				yield scrapy.Request(url = "http://www.thehindu.com/archive/web/"+single_date.strftime('%Y/%m/%d')+"/", callback=self.parse_day)


	def parse_day_old(self, response):
		sel_article = response.xpath('//li/a[contains(text(), "%s")]' % self.keyword).extract()
		for link in sel_article:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_article_old)

	def parse_day(self, response):
		sel_article = response.css('div.tpaper-container ul li a:contains("%s")' % self.keyword ).extract()
		for link in sel_article:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_article)

# http://www.thehindu.com/thehindu/2004/09/16/

	def parse_article_old(self, response):
		
		

	def parse_article(self, response):
		item = MyItem()
		item['link'] = response.url
		item['headline'] = response.xpath('//div[@class="article"]/h1[@class="title"]/text()').extract()
		if ( response.xpath('//div[@class="article"]/div[5][@class="lead-img-cont"]').extract() or\
			(response.xpath('//div[@class="article"]/div[5][@class="lead-img-cont lead-img-verticle"]').extract())):
			item['text'] = response.xpath('//div[@class="article"]/div[7]/p/text()').extract()
		else:
			item['text'] = response.xpath('//div[@class="article"]/div[6]/p/text()').extract()
		yield item
		

	
e'
