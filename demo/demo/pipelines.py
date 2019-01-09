# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DemoPipeline(object):

    def process_item(self, item, spider):
        print(spider, item)
        tpl = "%s\n%s\n\n" % (item['title'], item['href'])
        f = open('news.json', 'a')
        f.write(tpl)
        f.close()
        return item
