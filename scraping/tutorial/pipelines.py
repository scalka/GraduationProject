# -*- coding: utf-8 -*-
# project pipelines file
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv



class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class recipeExporter(object):

    def __init__(self):
        self.myCSV = csv.writer(open('recipe.csv', 'wb'))
        self.myCSV.writerow(['id', 'category','calories'])

    def process_item(self, item, spider):
     self.myCSV.writerow([item['id'].encode('utf-8'),
                                    item['category'].encode('utf-8'),
                                    item['calories'].encode('utf-8')])

     return item