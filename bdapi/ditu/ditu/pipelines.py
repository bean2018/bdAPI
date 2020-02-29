# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi

class DituPipeline(object):
    def __init__(self):
        dbparams = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '1234',
            'database': 'ditu',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['slng'], item['slat'],
                                       item['elng'], item['elat'], item['distance'], item['time']))
        self.conn.commit()
        print('finish')
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """insert into result(slng,slat,elng,elat,distance,time) values (%s,%s,%s,%s,%s,%s)"""
            return self._sql
        return self._sql





    # def process_item(self, item, spider):
    #     self.cursor.execute(self.sql, (item['title'], item['content'], item['author'], item['avatar'], item['pub_time'], item['origin_url'],item['article_id']))
    #     self.conn.commit()
    #     return item


    # def process_item(self, item, spider):
    #     return item
