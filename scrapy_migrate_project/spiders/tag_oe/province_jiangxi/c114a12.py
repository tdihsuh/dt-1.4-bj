# -*- coding: utf-8 -*-
import scrapy
from scrapy_migrate_project.items import crawler114
from bs4 import BeautifulSoup
import json
import sys
import time
class C114a12inSpider(scrapy.Spider):
    """江西经营异常列入名单"""
    name='c114a12in'
    allowed_domains = ['jx.gsxt.gov.cn']
    url = 'http://jx.gsxt.gov.cn/affichebase/queryAffichebase.do?noticetype=11&citycode=0&currentPage={}&search=&url=%2Faffichebase%2FqueryAffichebase.do%3Fnoticetype%3D11%26citycode%3D0'
    def start_requests(self):
        yield scrapy.Request(self.url.format(1))

    def parse(self, response):
        r=json.loads(response.text)
        totalpage=r['page']['totalPage']
        for page in range(1,2):
            yield scrapy.Request(self.url.format(page),
                                 dont_filter=True,
                                 callback=self.parseJson)
    def parseJson(self,response):
        r = json.loads(response.text)
        for each in r['data']:
            item=crawler114()
            item['notice_id']  = each['NOTICEID']
            item['punish_agent']  = each['JUDAUTH_CN']
            item['punish_date']  = each['NOTICEDATE']
            title = each['ENTNAME']
            item['entity_name'] = title.replace(u'关于', '').replace(u'列入经营异常名录公告', '')
            url='http://jx.gsxt.gov.cn/affichebase/queryAffichebaseFinallyDetails.do?noticeid={}&noticetype=11'
            yield scrapy.Request(url.format(item['notice_id']),
                                 meta={'item':item},
                                 dont_filter=True,
                                 callback=self.parseDetail)
    def parseDetail(self,response):
        soup = BeautifulSoup(response.text,'lxml')
        tag_p = soup.find_all('p')
        item=response.meta['item']
        # item['case_no'] = ''
        # item['punish_agent'] = ''
        # item['punish_date'] = ''
        # item['entity_name'] = ''
        # item['punish_reason'] = ''
        item['data_id'] = ''
        item['data_source'] = ''
        item['del_flag'] = ''
        item['op_flag'] = ''
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        # item['source_url'] = ''
        # item['source_page'] = ''
        item['reg_no'] = ''
        item['report_year'] = ''
        # item['spider_name'] = ''
        # item['notice_id'] = ''
        item['case_no'] = tag_p[0].get_text(strip=True)
        item['punish_reason'] = tag_p[2].get_text(strip=True)
        item['spider_name']=item['data_source']=self.name
        item['source_page']=response.text
        item['source_url']=response.url
        yield item
class C114a12outSpider(scrapy.Spider):
    """江西经营异常迁出名单"""

    name = 'c114a12out'
    allowed_domains = ['jx.gsxt.gov.cn']
    url = 'http://jx.gsxt.gov.cn/affichebase/queryAffichebase.do?noticetype=12&citycode=0&currentPage={}&search=&url=%2Faffichebase%2FqueryAffichebase.do%3Fnoticetype%3D11%26citycode%3D0'
    def start_requests(self):
        yield scrapy.Request(self.url.format(1))

    def parse(self, response):
        r=json.loads(response.text)
        totalpage=r['page']['totalPage']
        for page in range(1,1+totalpage):
            yield scrapy.Request(self.url.format(page),
                                 dont_filter=True,
                                 callback=self.parseJson)
    def parseJson(self,response):
        r = json.loads(response.text)
        for each in r['data']:
            item=crawler114()
            item['data_id'] = each['NOTICEID']
            item['release_org'] = each['JUDAUTH_CN']
            item['release_date'] = each['NOTICEDATE']
            title = each['ENTNAME']
            item['entity_name'] = title.replace(u'关于', '').replace(u'列入经营异常名录公告', '')
            url='http://jx.gsxt.gov.cn/affichebase/queryAffichebaseFinallyDetails.do?noticeid={}&noticetype=12'
            yield scrapy.Request(url.format(item['data_id']),
                                 meta={'item':item},
                                 dont_filter=True,
                                 callback=self.parseDetail)
    def parseDetail(self,response):
        soup = BeautifulSoup(response.text,'lxml')
        tag_p = soup.find_all('p')
        item=response.meta['item']
        # item['case_no'] = ''
        # item['release_org'] = ''
        # item['release_date'] = ''
        # item['entity_name'] = ''
        # item['release_reason'] = ''
        # item['data_id'] = ''
        # item['data_source'] = self.name
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        # item['source_url'] =response.url
        # item['source_page'] = ''
        item['reg_no'] = ''
        # item['spider_name'] = ''
        item['case_no'] = tag_p[0].get_text(strip=True)
        item['release_reason'] = tag_p[2].get_text(strip=True)
        item['spider_name']=item['data_source']=self.name
        item['source_page']=response.text
        item['source_url']=response.url
        yield item