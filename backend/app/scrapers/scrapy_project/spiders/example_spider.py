import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = ["https://example.com"]

    def parse(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "price": response.css(".price::text").get()
        }
