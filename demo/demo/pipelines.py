# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib

from demo import settings
import os
import re


class DemoPipeline(object):

    def process_item(self, item, spider):
        dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if spider.name == 'cnblogs':
            print(spider, item)
            tpl = "%s\n%s\n\n" % (item['title'], item['href'])
            f = open('news.json', 'a+')
            f.write(tpl)
            f.close()
            return item

        if spider.name == 'xiaohuar':
            # 无http前缀的链接需要拼接
            name = item['name']
            image_url = item['src']
            res = re.findall(r'/d/file/.*', image_url)
            if res:
                res = res[0]
                image_url = "http://www.xiaohuar.com" + res

            file_name = name + ".jpg"  # 图片名称
            print(file_name)
            file_path = '%s/%s' % (dir_path, file_name)
            # if os.path.exists(file_path):
            #     pass
            with open(file_path, 'wb') as file_writer:
                conn = urllib.request.urlopen(image_url)
                file_writer.write(conn.read())
            file_writer.close()

            return item