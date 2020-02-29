# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DituItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    slng = scrapy.Field()
    slat = scrapy.Field()
    elng = scrapy.Field()
    elat = scrapy.Field()
    distance = scrapy.Field()
    time = scrapy.Field()

