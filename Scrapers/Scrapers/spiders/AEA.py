import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Scrapers.items import ScrapersItem

class AeaSpider(CrawlSpider):
    name = "AEA"

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.3,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'FILES_STORE': "data/" + name
    }

    allowed_domains = ['www.aeaweb.org']
    start_urls = ['https://www.aeaweb.org/journals']

    rules = (
        Rule(LinkExtractor(allow=('.+\/journals\/[aA-zZ]+'),
                           deny=(
                               '.*search.*', '.+\/journals\/[aA-zZ]+\/.+', '.+subscriptions.*',
                               '.*get-journal-alerts.*', '.*policies.*', '.*data.*', '.*jstor.*')),
             callback=None, follow=True),
        Rule(LinkExtractor(allow=('.+\/issues\/[0-9]+', '.*\/issues'),
                           deny=(
                               '.+\/issues\/[0-9]+[?].*', '.+search.+',
                               '.+subscriptions.*')),
             callback='parse_item', follow=True))

    def parse_item(self, response):
        urls = []
        s = response.xpath('//article/h3[@class="title"]/a')
        if s:
            for i in s:
                urls.append(response.urljoin(i.attrib['href']))
        else:
            return
        item = ScrapersItem()
        item['file_urls'] = urls
        yield item
