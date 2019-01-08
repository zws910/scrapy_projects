# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector, XPathSelector

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://cnblogs.com/']

    def parse(self, response):
        hxs = Selector(response=response).xpath("//div[@class='post_item_body']")
        print(hxs)
        print("_____________________________")
        for obj in hxs:
            article_title = obj.xpath("./h3/a[@class='titlelnk']/text()").extract_first()
            print(article_title.strip())

