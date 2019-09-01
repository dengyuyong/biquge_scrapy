# -*- coding: utf-8 -*-
import scrapy
from biquge.items import FinctionItem
import re

class FinctionSpiderSpider(scrapy.Spider):
    name = 'Finction_spider'
    allowed_domains = ['biqugex.com']
    start_urls = ['http://biqugex.com/']

    def parse(self, response):
        nav_urls = response.xpath("//div[@class='nav']//a/@href").getall()
        for nav_url in nav_urls:
            if nav_url==r'/':
                yield scrapy.Request(url=response.url,callback=self.getCurrentPageFinctions)
            else:
                yield scrapy.Request(url=response.urljoin(nav_url), callback=self.getCurrentPageFinctions)


    def getCurrentPageFinctions(self,response):
        fincurls = set()
        Finction = response.xpath("//div[contains(@class,'wrap')]//a")
        # 得到网站当前页面所有的小说链接
        for finc in Finction:
            Fincurl = finc.xpath(".//@href").get()
            if 'book_' in str(Fincurl):
                fincurls.add(Fincurl)
        for url in fincurls:
            yield scrapy.Request(url=response.urljoin(url), callback=self.getFincInfo)

    def getFincInfo(self,response):
        #获取该小说的详细信息
        infos = response.xpath("//div[@class='info']")
        fincName = re.sub(r'\s','',infos.xpath(".//h2/text()").get())
        fincAuthor = re.sub(r'\s|作者：','',infos.xpath(".//div[@class='small']/span[1]/text()").get())
        fincType =re.sub(r'\s|分类：','',infos.xpath(".//div[@class='small']/span[2]/text()").get())
        fincStatus = re.sub(r'\s|状态：','',infos.xpath(".//div[@class='small']/span[3]/text()").get())
        fincWordCount = re.sub(r'\s|字数：','',infos.xpath(".//div[@class='small']/span[4]/text()").get())
        fincTime = re.sub(r'\s|更新时间：','',infos.xpath(".//span[@class='last'][1]/text()").get())
        fincIntro = re.sub(r'\s','',infos.xpath(".//div[@class='intro']/text()").get())
        fincUrl = response.url
        yield FinctionItem(fincName=fincName,
              fincAuthor=fincAuthor,
              fincType=fincType,
              fincStatus=fincStatus,
              fincWordCount=fincWordCount,
              fincTime=fincTime,
              fincIntro=fincIntro,
              fincUrl=fincUrl)

