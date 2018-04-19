This scrapy scrape the news article from Times of India website as per date and keyword pass while running the spider.

The data is stored in csv format with format as:
Date | Title | Article

So to run the spider you can switch to TOI folder and then execute the following command:
scrapy crawl toi -o Output/output_filename.csv -t csv

The total numbers of article I found while scraping from Jan-2001 to Apr-2018 is 2050 for HIV(keyword).

Package version:
1. scrapy 1.5.0
2. pandas 0.20.3
