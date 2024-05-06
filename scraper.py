import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
import os


class ComputerScienceSpyder(CrawlSpider):
    name = 'computerscience_data'
    allowed_domains = ['c-sharpcorner.com', 'wikipedia.org', 'javatpoint.com']
    custom_settings = {
        'CONCURRENT_REQUESTS': 8,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'DOWNLOAD_DELAY': 1.0,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 2,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 8,
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 1800,
    }

    def __init__(self, *args, **kwargs):
        super(ComputerScienceSpyder, self).__init__(*args, **kwargs)
        self.scraped_urls = set()

    def parsing_data_func(self, result):
        if result.url in self.scraped_urls:
            return
        self.scraped_urls.add(result.url)

        content = ' '.join(result.xpath('//p/text()').getall()).strip()

        src_list = result.css('img::attr(src)').extract()

        image_urls = []

        for url in src_list:
            full_url = result.urljoin(url)

            image_urls.append(full_url)

        yield {
            'Domain': result.url.split('/')[2],
            'URL': result.url,
            'Title': result.css('title::text').get(),
            'Content': content,
            'Image URLs': '|'.join(image_urls),
        }

        file_path = 'computerscience_data.csv'
        file_size_bytes = os.path.getsize(file_path)
        bytes_per_gigabyte = 1024 * 1024 * 1024
        file_size_gigabytes = file_size_bytes / bytes_per_gigabyte
        print(f"The file size is {file_size_gigabytes} GB")

        if file_size_gigabytes >= 0.5:
            raise CloseSpider("Done with Crawling")

    rules = (
        Rule(LinkExtractor(allow=()), callback='parsing_data_func', follow=True),
    )


process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'ROBOTSTXT_OBEY': True,
    'FEEDS': {
        'computerscience_data.csv': {
            'format': 'csv',
            'fields': ['Domain', 'Title', 'ParsedContent', 'ImageResourceLocator', 'ResourceLocator'],
        },
    },
})

# Start the crawling process for each domain
process.crawl(ComputerScienceSpyder, start_urls=[
    'https://www.javatpoint.com/javascript-tutorial'
    'https://www.javatpoint.com/c-programming-language-tutorial'
    'https://www.javatpoint.com/cloud-computing'
    'https://www.javatpoint.com/ajax-tutorial'
    'https://www.javatpoint.com/json-tutorial'
    'https://en.wikipedia.org/wiki/BERT_(language_model)'
    'https://en.wikipedia.org/wiki/Computer_vision'
    'https://www.c-sharpcorner.com/interview-questions-by-technology/android-programming'
    'https://www.c-sharpcorner.com/interview-questions-by-technology/dot_net_2015',
    'https://www.c-sharpcorner.com/interview-questions-by-technology/android-programming',
    'https://www.c-sharpcorner.com/interview-questions-by-technology/databases-and-dba',
    'https://www.c-sharpcorner.com/interview-questions-by-technology/ios',
    'https://en.wikipedia.org/wiki/C_Sharp_(programming_language)',
    'https://en.wikipedia.org/wiki/C%2B%2B',
    'https://en.wikipedia.org/wiki/U-Net',
])
process.start()
