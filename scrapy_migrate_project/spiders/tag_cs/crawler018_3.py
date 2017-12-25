# -*- coding: utf-8 -*-
# "采集证监会期货市场处罚信息"
import scrapy
from scrapy_migrate_project.items import Crawler018Item


# 页面改版，暂时不做
class ZjhQihuoSpider(scrapy.Spider):
    name = 'crawler018_3'
    allowed_domains = ['shixin.csrc.gov.cn']
    start_urls = ['http://shixin.csrc.gov.cn/honestypub//']

    # 按照关键词下载行政处罚信息
    def parse(self, response):
        pass
