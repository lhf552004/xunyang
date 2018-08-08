import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    addr = scrapy.Field()
    buildTime = scrapy.Field()
    houseType = scrapy.Field()