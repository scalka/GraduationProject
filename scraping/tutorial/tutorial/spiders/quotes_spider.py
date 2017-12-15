import scrapy


class QuotesSpider(scrapy.Spider):
    # identifies the Spider, unique in project
    name = "quotes"

    # must return an iterable of Requests, which the Spider will begin to crawl from
    def start_requests(self):
        urls = [
            'http://allrecipes.com/recipe/222191/lamb-braised-in-pomegranate/?internalSource=rotd&referringId=80&referringContentType=recipe%20hub',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # handle the response downloaded for each of the requests made
    # response is an instance of TextResponse and holds the page content and has further helpful methods to handle it
    # parse method is a scrapy default callback m., it parses the response, extracts the data as dicts and finds new URLs to follow and creates new requests from them
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)