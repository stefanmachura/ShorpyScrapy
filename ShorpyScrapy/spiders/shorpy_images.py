import scrapy

from scrapy.loader import ItemLoader
from ShorpyScrapy.items import ImageItem


class ImagesSpider(scrapy.Spider):
    name = "images"
    start_urls = [
        "https://www.shorpy.com/node?page=0",
    ]

    def parse(self, response):

        img_urls = response.css("h2.nodetitle a::attr(href)")
        yield from response.follow_all(img_urls, self.parse_node)

        next_page = response.css("a.pager-next::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_node(self, response):
        item = ItemLoader(item=ImageItem(), response=response)
        item.add_xpath("url", "//div[@class='content']/a/img/@src")
        item.add_xpath(
            "title", "normalize-space(//div[@class='content']/a/following-sibling::p)"
        )
        return item.load_item()
