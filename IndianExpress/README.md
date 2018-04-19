This scrapy scrape the news article from Indian Express website as per date and keyword pass while running the spider.

The data is stored in csv format with format as:
Date | Title | Article

So to run the spider you can switch to IndianExpress folder and then execute the following command:
scrapy crawl article -o Output/output_filename.csv -t csv

The total numbers of article I found while scraping from May-1997 o Feb-2014 is 780.

Package version:
1. scrapy 1.5.0
