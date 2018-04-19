Using Scrapy the following newspaper are being scraped,
1. Indian Express
2. Times of India
3. The Hindu

For each newspaper a different scrapy project is created with their respective names.
Afer running or crawling the spider the output is in form t
Article is the whole story of that article

By going inside the each newspaper (for eg. cd TOI/) you can then execute the following command

scrapy crawl spider_name -o Output/file_name.csv -t csv

Required packages:
1. Scrapy 1.5.0
2. pandas 0.20.3
