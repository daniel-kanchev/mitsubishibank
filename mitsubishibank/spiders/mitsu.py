import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from mitsubishibank.items import Article


class MitsuSpider(scrapy.Spider):
    name = 'mitsu'
    start_urls = ['https://www.tr.mufg.jp/english/pressreleases/pressreleases.html']

    def parse(self, response):
        articles = response.xpath('//div[@class="newRow"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article.xpath('.//p[@class="mod-link"]/a/text()').get()
            if title:
                title = title.strip()

            date = article.xpath('.//div[@class="dayCell"]/text()').get()
            if date:
                date = datetime.strptime(date.strip(), '%b. %d, %Y')
                date = date.strftime('%Y/%m/%d')

            link = article.xpath('.//p[@class="mod-link"]/a/@href').get()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('link', response.urljoin(link))

            yield item.load_item()
