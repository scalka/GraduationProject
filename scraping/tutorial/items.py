# -*- coding: utf-8 -*-
# project items definition file
# Defines the models for scraped items

import scrapy
# recipe model
class Recipe(scrapy.Item):
    # defines the fields for item
    id = scrapy.Field()
    category = scrapy.Field()
    calories = scrapy.Field()
    pass
# rating model
class Rating(scrapy.Item):
    id = scrapy.Field()
    user = scrapy.Field()
    rating = scrapy.Field()
    category = scrapy.Field()
    calories = scrapy.Field()
    pass

