import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Scrapers.items import ScrapersItem


class CSHSpider(CrawlSpider):
    name = "CSH"

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'FILES_STORE': "data/" + name,
        'LOG_FILE': "log/" + name + ".log",
    }

    start_urls = ['https://www.cshl.edu/cold-spring-harbor-laboratory-press/journals/']

    rules = (
        Rule(LinkExtractor(allow=('.*\w+\.cshlp\.org$'),
                           deny=('intl')),
             callback=None, follow=True),
        Rule(LinkExtractor(allow=('\/content\/by\/year$'),
                           deny=()),
             callback=None, follow=True),
        Rule(LinkExtractor(allow=('\/content\/by\/year\/\d+$'),
                           deny=()),
             callback=None, follow=True),
        Rule(LinkExtractor(allow=('\/content\/vol\d+\/issue\d+\/$', '\/content\/vol\d+\/issue\d+\/index\.dtl$',
                                  '\/content\/vol\d+\/issue\d+-\d+\/$', '\/content\/vol\d+\/issue\d+-\d+\/index\.dtl$'),
                           deny=()),
             callback='parse_item', follow=False)
    )

    def parse_item(self, response):
        urls = []
        s = response.xpath('//ul[@class="cit-views"]/li[@class="first-item"]/a')
        if s:
            for i in s:
                urls.append(response.urljoin(i.attrib['href']))
        else:
            return
        item = ScrapersItem()
        item['file_urls'] = urls
        print(response.xpath('//title/text()').get())
        yield item
