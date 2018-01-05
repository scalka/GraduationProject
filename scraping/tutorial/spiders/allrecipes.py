import scrapy
from scrapy import signals
from tutorial.items import Recipe, Rating

class RecipesSpider(scrapy.Spider):
    # identifies the Spider, unique in project
    name = "all-recipes"
    """
    start_urls = [
        'http://allrecipes.com/recipe/222191/',
        'http://allrecipes.com/recipe/241480/',
    ]
    """
    start_urls = ['http://allrecipes.com/recipe/%s/' % page for page in range(6664,258791)]
    # handle the response downloaded for each of the requests made
    # response is an instance of TextResponse and holds the page content and has further helpful methods to handle it
    # parse method is a scrapy default callback m., it parses the response, extracts the data as dicts and finds new URLs to follow and creates new requests from them
    def parse(self, response):
        for item in response.css('div.recipe-container-outer'):
            recipe = Recipe()
            recipe['id'] = response.url
            recipe['category'] = item.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "toggle-similar__title", " " ))]//text() ').extract()[2].strip()
            recipe['calories'] = item.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "calorie-count", " " ))]//span //text() ').extract_first()
            print( recipe['category'])
            yield recipe


class RatingSpider(scrapy.Spider):
    name = "all-ratings"
    start_urls = ['http://allrecipes.com/recipe/%s/' % page for page in range(12895, 258791)]
    # for user in response.css('review-container clearfix'):
    def parse(self, response):
        for user in response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "review-container", " " ))]'):
            rating = Rating()
            rating['id'] = response.url
            rating['user'] = user.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "cook-info", " " ))] //h4  //text() ').extract_first()
            rating['rating'] = user.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "stars-and-date-container", " " ))] //span /@class ').extract_first()
        for item in response.css('div.recipe-container-outer'):
            rating['category'] = item.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "toggle-similar__title", " " ))]//text() ').extract()[2].strip()
            rating['calories'] = item.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "calorie-count", " " ))]//span //text() ').extract_first()
        yield rating
