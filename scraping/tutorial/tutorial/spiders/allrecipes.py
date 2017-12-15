import scrapy


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
        for recipe in response.css('div.quote'):
            yield {
                'title': recipe.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "recipe-summary__h1", " " ))]/text()').extract_first(),
                'ingredients': recipe.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "step", " " )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "recipe-directions__list--item", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "added", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "recipe-summary__h1", " " ))]/text()').extract_first(),
                'directions': recipe.css('div.tags a.tag::text').extract(),
            }