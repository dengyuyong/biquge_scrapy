# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import configparser
import json
import pymysql

import redis

class BiqugeRedisPipeline(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(r'D:\python_project_path\scrapy_Demo\biquge\biquge\redis_config.txt')
        host = self.config.get('redis','host')
        port = self.config.get('redis','port')
        self.pool = redis.ConnectionPool(host=host,port=port,max_connections=10000)#连接池
        self.redisConn =redis.Redis(connection_pool=self.pool)

    def process_item(self, item, spider):
        self.redisConn.execute_command('select 2') #切换db数据库
                                                                  #dumps默认中文为ascii码  ensure_ascii改成中文编码
        self.redisConn.set(item['fincName'],json.dumps(dict(item),ensure_ascii=False),nx=True)#   nx--->key不存在时添加数据
        return item

class BiqugeMySqlPipeline(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(r'D:\python_project_path\scrapy_Demo\biquge\biquge\redis_config.txt')
        host = self.config.get('mysql','host')
        port = self.config.get('mysql','port')
        user = self.config.get('mysql','user')
        password = self.config.get('mysql','password')
        charset = self.config.get('mysql','charset')
        db = self.config.get('mysql','db')
        self.mysqlCon = pymysql.connect(host=host,port=int(port),user=user,password=password,charset=charset,database=db)
        self.cursor = self.mysqlCon.cursor()

    # def open_spider(self,spider):
    def process_item(self, item, spider):
        if self.select_fincExists(item) is None:
            fincName = item['fincName']
            fincAuthor = item['fincAuthor']
            fincType = item['fincType']
            fincStatus = item['fincStatus']
            fincWordCount = item['fincWordCount']
            fincTime = item['fincTime']
            fincIntro = item['fincIntro']
            fincUrl = item['fincUrl']
            sql="""
            insert into fincinfo(fincName,fincAuthor,fincType,fincStatus,fincWordCount,fincTime,fincIntro,fincUrl) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
            """.format(fincName,fincAuthor,fincType,fincStatus,fincWordCount,fincTime,fincIntro,fincUrl)
            self.cursor.execute(sql)
            self.mysqlCon.commit()
        return item

    #查询这条数据是否存在
    def select_fincExists(self,item):
        fincName = item['fincName']
        fincAuthor = item['fincAuthor']
        sql = """select fincName from fincInfo where fincName='{0}' and fincAuthor='{1}' limit 1""".format(fincName,fincAuthor)
        self.cursor.execute(sql)
        resultNumber = self.cursor.fetchone()#返回查询单个结果
        return resultNumber

    def close_spider(self,spider):
        self.cursor.close()
        self.mysqlCon.close()