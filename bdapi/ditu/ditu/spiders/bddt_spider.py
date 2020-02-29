import json,pymysql
import scrapy, os, urllib.request, threading, time
from ditu.items import DituItem

class bddtSpider(scrapy.Spider):
    name = 'ditu'  # 名字必须是唯一的，用来确认蜘蛛的名字
    allowed_domains = ['api.map.baidu.com'] # 限定爬虫的范围

    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='ditu', port=3306, charset='utf8')
    cur = conn.cursor()  # 获取一个游标
    sql = " select count(*) from `result` "
    cur.execute(sql)
    data = cur.fetchall()
    now = data[0][0]
    cur.close()  # 关闭游标
    conn.close()  # 释放数据库资源

    conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='ditu', port=3306, charset='utf8')
    cur = conn.cursor()  # 获取一个游标

    sql = " select * from `coordinate` where id = %s "
    cur.execute(sql, now + 1)
    cor = cur.fetchall()[0]
    st = str(cor[2]) + ',' + str(cor[1])
    en = str(cor[4]) + ',' + str(cor[3])
    print(st, en)

    mode = 'driving'
    ak = ''

    start_urls = [
        # 'http://api.map.baidu.com/directionlite/v1/{mode}?origin={origin}&destination={destination}&ak={ak}'\
        # .format(mode=p['mode'], origin=p['origin'], destination=p['destination'],ak=p['ak'])
        # 'http://api.map.baidu.com/directionlite/v1/driving?origin=37.42827115,118.445386&destination=37.53668887,118.5384035&ak=v3coGHijWgQ01endbgY7XV3EMaPEwIUh'

        'http://api.map.baidu.com/directionlite/v1/{mode}?origin={origin}&destination={destination}&ak={ak}' \
        .format(mode=mode, origin=st, destination=en, ak=ak)
    ]


    def parse(self, response):  # 分析的方法
        result = json.loads(response.text)['result']

        item = DituItem()
        item['slng'] = float(result['origin']['lng'])
        item['slat'] = float(result['origin']['lat'])
        item['elng'] = float(result['destination']['lng'])
        item['elat'] = float(result['destination']['lat'])
        item['distance'] = float(result['routes'][0]['distance'])
        item['time'] = float(result['routes'][0]['duration'])
        yield item

        conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='ditu', port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标

        sql = " select count(*) from `result` "
        cur.execute(sql)
        data = cur.fetchall()
        now = data[0][0]
        cur.close()  # 关闭游标
        conn.close()  # 释放数据库资源

        conn = pymysql.connect(host='localhost', user='root', passwd='1234', db='ditu', port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标
        # sql = "SELECT * FROM `coordinate` WHERE id > %s"
        # cur.execute(sql, 2)
        sql = " select * from `coordinate` where id = %s "
        cur.execute(sql, now+1)
        cor = cur.fetchall()[0]
        st = str(cor[2]) + ',' + str(cor[1])
        en = str(cor[4]) + ',' + str(cor[3])

        mode = 'driving'
        ak = 'v3coGHijWgQ01endbgY7XV3EMaPEwIUh'

        if st:
            uu = 'http://api.map.baidu.com/directionlite/v1/{mode}?origin={origin}&destination={destination}&ak={ak}' \
                .format(mode=mode, origin=st, destination=en, ak=ak)
            yield scrapy.Request(uu, callback=self.parse, dont_filter=True)


        #