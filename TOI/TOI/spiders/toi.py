# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from datetime import timedelta, date
import datetime

class MyItem(scrapy.Item):
	Title = scrapy.Field()
	Date = scrapy.Field()
	article = scrapy.Field()

def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days)):
		yield start_date + timedelta(n)

class ToiSpider(scrapy.Spider):
	name = 'toi'
	allowed_domains = ['timesofindia.indiatimes.com']
#	start_urls = ['https://timesofindia.indiatimes.com/2009/1/1/archivelist/year-2009,month-1,starttime-%d.cms' % page for page in range(39814,40543)]
	keyword = input("Enter the keyword to be scrape: ")

	def start_requests(self):
		
		min_date = datetime.datetime.strptime('1/1/2001', '%d/%m/%Y')
		prev_day = (date.today()-timedelta(2)).strftime('%d/%m/%Y')
		max_date = datetime.datetime.strptime(prev_day, '%d/%m/%Y')
		
		while True:
			try:
				start_date = datetime.datetime.strptime(input('Enter start date (dd/mm/yyyy): '), '%d/%m/%Y')
				if (start_date < min_date or start_date > max_date):
					print('Enter the date between '+ min_date.date().strftime('%d/%m/%Y') + ' to ' + max_date.date().strftime('%d/%m/%Y') + '.')
					continue
				else:
					break
			except ValueError:
				print('Invalid Date')
		
		while True:
			try:
				end_date = datetime.datetime.strptime(input('Enter end date (dd/mm/yyyy): '), '%d/%m/%Y')
				if (end_date < min_date or end_date > max_date):
					print('Enter the date between '+ min_date.date().strftime('%d/%m/%Y') + ' to ' + max_date.date().strftime('%d/%m/%Y') + '.')
				elif ( end_date < start_date):
					print("End date can't be less than start date")
					continue				
				else:
					break
			except ValueError:
				print('Invalid Date')
			
		start = pd.datetime(2001,1,1).date()
		end = (date.today()-timedelta(2))
		# period = int((end-start).days)
		N = int((end-start).days+1)
		data = pd.DataFrame({'A': range(36892, 36892+N)}, index=pd.date_range(start=start, end=end, freq='D'))
		
		start_date = start_date.strftime('%Y-%m-%d')
		end_date = end_date.strftime('%Y-%m-%d')
		start_page_no = data.ix[start_date, 'A']
		end_page_no = data.ix[end_date, 'A']
		urls = ['https://timesofindia.indiatimes.com/2009/1/1/archivelist/year-2009,month-1,starttime-%d.cms' % page for page in range(start_page_no,end_page_no+1)]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse_day)

	def parse_day(self, response):
		sel_article = response.xpath('//span/a[contains(text(), "'+self.keyword+'")]')
		sel_link = sel_article.xpath('@href').extract()
		
		for link in sel_link:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_article)

	def parse_article(self, response):
		item = MyItem()
		item['Title'] = response.xpath('//section/h1/text()').extract()
		item['Date'] = response.xpath('//section/span/span/text()').extract()
		if response.xpath('//arttextxml/text()'):
			item['article'] = response.xpath('//arttextxml/text()').extract()
		elif response.css('div.Normal span::text'):
			item['article'] = response.css('div.Normal span::text').extract()
		else:
			item['article'] = response.css('div.Normal::text').extract()
		yield item
		

	

