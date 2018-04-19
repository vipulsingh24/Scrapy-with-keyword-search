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

class ArticleSpider(scrapy.Spider):

	name = 'article'
	allowed_domains = ['archive.indianexpress.com']
	start_urls = ['http://archive.indianexpress.com/']
	keyword = input("Enter the keyword to be scrape: ")

	def start_requests(self):
		
		min_date = datetime.datetime.strptime('1/5/1997', '%d/%m/%Y')
		max_date = datetime.datetime.strptime('28/2/2014', '%d/%m/%Y')

		while True:
			try:
				start_date = datetime.datetime.strptime(input('Enter start date (dd/mm/yyyy): '), '%d/%m/%Y')
				if (start_date < min_date or start_date > max_date):
					print('Enter the date between range 1/5/1997 to 28/2/2014')
					continue
				else:
					break
			except ValueError:
				print('Invalid Date')
		
		while True:
			try:
				end_date = datetime.datetime.strptime(input('Enter end date (dd/mm/yyyy): '), '%d/%m/%Y')
				if (end_date < min_date or end_date > max_date):
					print('Enter the date between range 1/5/1997 to 28/2/2014')
				elif ( end_date < start_date):
					print("End date can't be less than start date")
					continue				
				else:
					break
			except ValueError:
				print('Invalid Date')
			
		
		for single_date in daterange(start_date, end_date):
			if ( single_date < datetime.datetime.strptime('11/3/2006', '%d/%m/%Y') ):
				yield scrapy.Request(url = "http://archive.indianexpress.com/archive/news/"+single_date.strftime('%-d/%-m/%Y')+"/", callback=self.parse_day_old)
			else:
				yield scrapy.Request(url = "http://archive.indianexpress.com/archive/news/"+single_date.strftime('%-d/%-m/%Y')+"/", callback=self.parse_day)

	def parse_day_old(self, response):
		sel_article = response.xpath('//div[@class="news_head"]/ul/li/a/@href').re('\s*(.*)')
		for link in sel_article:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_article)

	def parse_day(self, response):
		#sel_article = response.xpath('//div[@class="news_head"]/ul/li/a/@href').re('\s*(.*)')
		sel_article = response.xpath('//div[@class="news_head"]/ul/li/a/@href').extract()
		for link in sel_article:
			yield scrapy.Request(response.urljoin(link+'0'), callback=self.parse_article)

	def parse_article(self, response):
		item = MyItem()
		pres_old = response.css('div.top_head h2::text').re(r'%s' % self.keyword)
		pres = response.xpath('//*[@id="ie2013-content"]/h1/text()').re(r'%s' % self.keyword)
		#pres = response.xpath('//*[@id="ie2013-content"]/h1/text()').re(r'HIV')
		if pres:
			item['Title'] = response.xpath('//*[@id="ie2013-content"]/h1/text()').extract()
			item['Date'] = response.xpath('//*[@id="ie2013-content"]/div[1]/text()').extract()
			item['article'] = response.xpath('//*[@id="ie2013-content"]/div[@class="ie2013-contentstory"]/text() | //*[@id="ie2013-content"]/div[@class="ie2013-contentstory"]/p/text()').extract()
			yield item
		elif pres_old:
			item['Title'] = response.css('div.top_head h2::text').extract()
			item['Date'] = response.xpath('//div[@class="posted"]/strong/text() | //div[@class="posted"]/strong/span/text()').extract()
			item['article'] = response.css('div.txt p::text').extract()
			yield item
		else:
			pass
		

	

