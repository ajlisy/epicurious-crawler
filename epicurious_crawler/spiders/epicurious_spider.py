import scrapy

from epicurious_crawler.items import Recipe

class EpiSpider(scrapy.Spider):
    name = "epicurious"
    allowed_domains = ["epicurious.com"]
    start_urls = [
        "http://www.epicurious.com/recipes/food/views/shrimp-olivier-51259620",
    ]

    def parse(self,response):
        relatedContent=response.xpath("//*[contains(@class,'relatedContent')]/div[@class='recipes']/ul/li/a/@href")
        for href in relatedContent:
            url=response.urljoin(href.extract())
            yield scrapy.Request(url,callback=self.parse_recipe)


    def parse_recipe(self,response):
        item=Recipe()
        item['title']=response.xpath("//title/text()").re('(.+) \| Epic.*')
        item['ingredientsArray']=[]
        for ingredient in response.xpath("//li[contains(@itemprop,'ingredients')]/text()"):
            item['ingredientsArray'].append(ingredient.extract())
        yield item