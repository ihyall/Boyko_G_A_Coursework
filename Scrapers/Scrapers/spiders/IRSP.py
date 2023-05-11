import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Scrapers.items import ScrapersItem
import re


class IRSPSpider(CrawlSpider):
    name = "IRSP"

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'FILES_STORE': "data/" + name,
    }

    allowed_domains = ['www.int-res.com']
    start_urls = ['https://www.int-res.com/home/']

    rules = (
        Rule(LinkExtractor(allow=('journals/[a-z]+\/[a-z]+-home\/$'),
                           deny=()),
             callback=None, follow=True),
        Rule(LinkExtractor(allow=('abstracts\/[a-z]+\/v\d+\/?$', 'abstracts\/[a-z]+\/v\d+-\d+\/?$',
                                  'abstracts\/[a-z]+\/v\d+\/?n\d+$', 'abstracts\/[a-z]+\/v\d+\/?n\d+-\d+$'),
                           deny=()),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        urls = []
        s = response.xpath('//div[@class="journal-index"]//a[not(@class)]')
        if s:
            for i in s:
                if not '.pdf' in i.attrib['href'] and not 'feature' in i.attrib['href']:
                    urls.append(response.urljoin(i.attrib['href']))
        else:
            return
        item = ScrapersItem()
        item['file_urls'] = urls
        yield item

