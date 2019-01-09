# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector, XPathSelector
from scrapy.http import Request
from demo.items import CnblogsItem

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://cnblogs.com/']

    visited_urls = []

    def parse(self, response):
        # 获取标题
        hxs = Selector(response=response).xpath("//div[@class='post_item_body']")
        for obj in hxs:
            article_title = obj.xpath("./h3/a[@class='titlelnk']/text()").extract_first().strip()
            href = obj.xpath("./h3/a[@class='titlelnk']/@href").extract_first().strip()
            item_obj = CnblogsItem(title=article_title, href=href)
            yield item_obj

        # 获取页码对应的url
        # urls = Selector(response=response).xpath("//div[@id='paging_block']//a/@href").extract()
        # urls = Selector(response=response).xpath("//a[starts-with(@href, '/sitehome/p/')]/@href").extract()  # 以什么开头
        urls = Selector(response=response).xpath("//a[re:test(@href, '/sitehome/p/\d+')]/@href").extract()  # 通过正则匹配
        for url in urls:
            # url可能过长, 为方便存储用md5加密
            md5_url = self.md5(url)
            if md5_url in self.visited_urls:
                # print('%s already existed.' % url)
                pass
            else:
                self.visited_urls.append(md5_url)
                print(url)
                url = "http://cnblogs.com/" + url
                # 将要访问的url给调度器
                yield Request(url=url, callback=self.parse)  # 写了yield会默认发给调度器

    def md5(self, url):
        import hashlib
        obj = hashlib.md5()
        obj.update(bytes(url, encoding='utf8'))
        return obj.hexdigest()