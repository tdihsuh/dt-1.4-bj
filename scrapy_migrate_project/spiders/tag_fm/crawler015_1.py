# -*- coding: utf-8 -*-
# "采集国家食药监局的违法广告数据"
import json
import re

import scrapy
import time
from bs4 import BeautifulSoup
from scrapy_migrate_project.items import Crawler015Item



class GovMedIllegalAdvSpider(scrapy.Spider):
    name = 'crawler015_1'
    allowed_domains = ['sfda.gov.cn']
    start_urls = ['http://www.sfda.gov.cn/WS01/CL1826/index.html']

    # 列表页
    def parse(self, response):
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        tag = soup.find(name='td', class_='2016_erji_content').contents[0]
        trnodes = tag.find_all(name='tr')

        for node in (trnodes):
            dist_nodes = node.find_all(name='td', class_='distance15')
            if (dist_nodes == None or len(dist_nodes) < 1):
                # 处理当前节点，获取超链接、标题和发布日期
                item = Crawler015Item()
                link_node = node.find(name='a')
                link = link_node.get('href')
                link ='http://www.sfda.gov.cn/WS01/' + link.replace('../', '')
                item['title'] = link_node.text.encode('utf-8').strip()
                pub_node = node.find(name='span')
                item['pub_date'] = pub_node.text.encode('utf-8').replace(')', '').replace('(', '').replace('\r\n','')
                yield scrapy.Request(link,
                                     callback=self.parse_detail,
                                     meta= {'item':item})
        # 翻页
            # 总页数
        tag = soup.find(class_='pageTdSTR15')
        page_num = 1
        page_str = tag.text.encode('utf-8').split('/')  # 第1页/共5页
        pattern = re.compile(r'[0-9]+')
        match = re.search(pattern, page_str[1])
        if match:
            page_num = int(match.group())

        for i in range(1, page_num, 1):
            url = 'http://www.sfda.gov.cn/WS01/CL1850/index_' + str(i) + '.html'
            yield scrapy.Request(url,
                                 callback=self.parse)

    # 详情页
    def parse_detail(self, response):
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        item = response.meta['item']
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        item['source_page'] = data
        # 从header中提取最后Last-modified信息
        last_modified = response.headers['Last-modified']
        if (last_modified == None or len(last_modified) == 0):
            last_modified = response.headers['If-Modified-Since']

        # 提取数据
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        tag = soup.find(name='td', class_='articlecontent3')
        item['content'] = tag.text.encode('utf-8').strip()
        href_nodes = tag.find_all(name='a')
        item['attach_flag'] = '0'
        if (href_nodes != None and len(href_nodes) > 0):
            item['attach_flag'] = '1'
        yield item
