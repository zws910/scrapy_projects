# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector, XPathSelector
from scrapy.http import Request
from demo.items import XiaohuarItem
import re


class XiaohuarSpider(scrapy.Spider):
    name = 'xiaohuar'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/list-1-0.html']

    visited_pages = []

    def parse(self, response):
        item = XiaohuarItem()
        # 获取page_url
        page_urls = Selector(response=response).xpath("//a[re:test(@href, 'http://www.xiaohuar.com/list-\d+-\d+.html')]/@href").extract()
        for page_url in page_urls:
            md5_page_url = self.md5(page_url)
            if page_url in self.visited_pages:
                pass
            else:
                self.visited_pages.append(page_url)
                # print(page_url)
                yield Request(url=page_url, callback=self.parse)



        # 获取图片url
        hxs = Selector(response=response).xpath("//a[re:test(@href, 'http://www.xiaohuar.com/p-\d+-\d+.html')]")
        for obj in hxs:
            img_url = obj.xpath("./img/@src").extract_first()
            name = obj.xpath("./img/@alt").extract_first()
            if img_url and name:
                item['src'] = img_url
                item['name'] = name
                yield item

    def md5(self, url):
        import hashlib
        obj = hashlib.md5()
        obj.update(bytes(url, encoding='utf-8'))
        return obj.hexdigest()