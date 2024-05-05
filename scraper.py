import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
import os

class ExtendedEduSpider(CrawlSpider):
    name = 'extended_education_spider'
    allowed_domains = ['geeksforgeeks.org', 'wikipedia.org', 'w3schools.com']
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,  # Increase concurrency with multiple threads
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,  # Limit concurrency per domain
        'DOWNLOAD_DELAY': 0.5,  # Reduce delay between requests
        'AUTOTHROTTLE_ENABLED': True,  # Automatically adjust crawling speed
        'AUTOTHROTTLE_START_DELAY': 1,  # Initial delay for autothrottle
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 16,  # Target concurrency level
        'HTTPCACHE_ENABLED': True,  # Enable HTTP caching
        'HTTPCACHE_EXPIRATION_SECS': 3600,  # Cache expiration time (in seconds)
    }

    def __init__(self, *args, **kwargs):
        super(ExtendedEduSpider, self).__init__(*args, **kwargs)
        self.scraped_urls = set()

    def parse_item(self, response):
        if response.url in self.scraped_urls:
            return
        self.scraped_urls.add(response.url)

        content = ' '.join(response.xpath('//p/text()').extract()).strip()
        image_urls = [response.urljoin(url) for url in response.css('img::attr(src)').extract()]
        yield {
            'Domain': response.url.split('/')[2],
            'URL': response.url,
            'Title': response.css('title::text').get(),
            'Content': content,
            'Image URLs': '|'.join(image_urls),
        }

        # Check the size of the output file
        file_size = os.path.getsize('educational_data.csv') / (1024 * 1024 * 1024)  # Convert bytes to gigabytes
        if file_size >= 0.5:  # Stop spider after collecting 1GB of data
            raise CloseSpider(reason='Reached 1GB limit')

    # Define rules to follow links
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )

# Configure the output and other settings
process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'ROBOTSTXT_OBEY': True,
    'FEEDS': {
        'educational_data.csv': {
            'format': 'csv',
            'fields': ['Domain', 'URL', 'Title', 'Content', 'Image URLs'],
        },
    },
})

# Start the crawling process for each domain
process.crawl(ExtendedEduSpider, start_urls=[
    'https://www.geeksforgeeks.org/data-structures/',
    'https://en.wikipedia.org/wiki/Artificial_intelligence',
    'https://www.w3schools.com/js/default.asp',
    'https://www.w3schools.com/sql/default.asp',
    'https://www.w3schools.com/python/default.asp',
    'https://www.w3schools.com/java/default.asp',
    'https://www.w3schools.com/php/default.asp',
    'https://www.w3schools.com/c/index.php',
    'https://www.geeksforgeeks.org/machine-learning/',
    'https://www.geeksforgeeks.org/python-mongodb-tutorial/',
    'https://www.geeksforgeeks.org/system-design-tutorial/',
    'https://www.geeksforgeeks.org/web-design/',
    'https://en.wikipedia.org/wiki/Data_mining',
    'https://en.wikipedia.org/wiki/Information_retrieval',
    'https://en.wikipedia.org/wiki/Natural_language_processing',
])
process.start()
