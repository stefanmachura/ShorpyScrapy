import scrapy
from itemloaders.processors import TakeFirst


class ImageItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
