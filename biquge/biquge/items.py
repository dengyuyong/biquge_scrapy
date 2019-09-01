# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FinctionItem(scrapy.Item):
    fincName=scrapy.Field()
    fincAuthor=scrapy.Field()
    fincType=scrapy.Field()
    fincStatus=scrapy.Field()
    fincWordCount=scrapy.Field()
    fincTime=scrapy.Field()
    fincIntro=scrapy.Field()
    fincUrl=scrapy.Field()