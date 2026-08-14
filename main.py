import json

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import signals



quotes = []
authors = []

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):

        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(
            collect_item,
            signal=signals.item_scraped
        )

        return spider
    
    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):

            data = {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }

            about_link = quote.xpath('.//span/a/@href').get()

            if about_link:
                yield scrapy.Request(
                    response.urljoin(about_link),
                    callback=self.parse_author
                )
                
            yield data
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(
                response.urljoin(next_link),
                callback=self.parse
            )


    def parse_author(self, response):

        author = {
            "fullname" : response.xpath(
                '//h3[@class="author-title"]/text()'
            ).get(),

            "born_date" : response.xpath(
                '//span[@class="author-born-date"]/text()'
            ).get(),

            "born_location" : response.xpath(
                '//span[@class="author-born-location"]/text()'
            ).get(),

            "description" : response.xpath(
                '//div[@class="author-description"]/text()'
            ).get().strip(),
        }
        yield author

def collect_item(item, response, spider):
    item = dict(item)

    if "quote" in item:
        quotes.append(item)

    if "fullname" in item:
        authors.append(item)

if __name__ == "__main__":
    process = CrawlerProcess(
        settings = {
            "LOG_LEVEL":"ERROR"
        }
    )
    process.crawl(QuotesSpider)
    process.start()

    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(
            quotes,
            file,
            ensure_ascii=False,
            indent=4
        )

    with open("authors.json", "w", encoding="utf-8") as file:
        json.dump(
            authors,
            file,
            ensure_ascii=False,
            indent=4
        )
