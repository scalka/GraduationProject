import scrapy
from tutorial.items import Recipe, Rating


class QuotesSpider(scrapy.Spider):
    # identifies the Spider, unique in project
    name = "allrecipes"

    start_urls = [
        'http://allrecipes.com/recipe/222191/lamb-braised-in-pomegranate/?internalSource=rotd&referringId=80&referringContentType=recipe%20hub',
        'http://allrecipes.com/recipe/241480/braised-lamb-shoulder-chops/?internalSource=similar_recipe_banner&referringId=222191&referringContentType=recipe&clickId=simslot_1',
    ]

    # handle the response downloaded for each of the requests made
    # response is an instance of TextResponse and holds the page content and has further helpful methods to handle it
    # parse method is a scrapy default callback m., it parses the response, extracts the data as dicts and finds new URLs to follow and creates new requests from them
    def parse(self, response):
        for item in response.css('div.recipe-container-outer'):
            recipe = Recipe()
            recipe['id'] = response.url
            recipe['category'] = item.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "toggle-similar__title", " " ))]//text() ').extract()[2]
            recipe['calories'] = item.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "calorie-count", " " ))]//span //text() ').extract_first()
            yield recipe

        more_reviews = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "btns-one-small", " " ))]')

        for user in response.css('div.recipe-container-outer'):
            rating = Rating()
            rating['id'] = response.url
            rating['user'] = item.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cook-info", " " ))] //h4  //text() ').extract()
            rating['rating'] =item.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "stars-and-date-container", " " ))] //span /@class ').extract()
            yield rating