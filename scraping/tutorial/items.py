# -*- coding: utf-8 -*-
# project items definition file
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Recipe(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    category = scrapy.Field()
    calories = scrapy.Field()
    pass

class Rating(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    user = scrapy.Field()
    rating = scrapy.Field()
    pass