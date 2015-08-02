import scrapy

from epicurious_crawler.items import Recipe

class EpiSpider(scrapy.Spider):
    name = "epicurious"
    allowed_domains = ["epicurious.com"]
    start_urls = [
        "http://www.epicurious.com/recipes/food/views/shrimp-olivier-51259620",
    ]

    def parse(self,response):
        item=Recipe()
        item['title']=response.xpath("//title/text()").re('(.+) \| Epic.*')
        item['ingredientsArray']=[]
        for ingredient in response.xpath("//li[contains(@itemprop,'ingredients')]/text()"):
            item['ingredientsArray'].append(ingredient.extract())
        yield item