# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_migrate_project.items import crawler116
from bs4 import BeautifulSoup
import requests
import re

class C116a07inSpider(scrapy.Spider):
    name = 'c116a07in'
    allowed_domains = ['*']
    url='http://xyhn.hainan.gov.cn/JRBWeb/jointCredit/HnZsXzcfxxSjbzMainController.do?reqCode=getXzcfInfo&pageIndex={}&pageSize={}&isIndex=2'
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Host': 'xyhn.hainan.gov.cn',
        'Referer': 'http://hn.gsxt.gov.cn/notice/search/ent_announce',
        'Connection':'keep-alive',
        'X-Requested-With':'XMLHttpRequest'
        }
    patt = re.compile(r'\d+\.\d+\.\d+\.\d+')
    def start_requests(self):

        yield scrapy.Request(self.url.format(1,1),
                             # headers=self.headers,
                             )

    def parse(self, response):
        if not self.patt.search(response.text):
            r=json.loads(response.text.split('</script>')[-1])
            # print('======================',r,'=========================')
            datasize=r.get('dataSize')
            pageSize=5000
            totalpages=datasize//pageSize if datasize%pageSize==0 else datasize//pageSize+1

            print(totalpages,type(totalpages))
            for page in range(1,2):
                yield scrapy.Request(self.url.format(page,pageSize),
                                     dont_filter=True,
                                     callback=self.parseJson)
        else:
            print('=====================ip blocked========================')
            print(self.patt.search(response.text).group(1))
    def parseJson(self,response):
        # patt=re.compile(r'\d+\.\d+\.\d+\.\d+')
        if not self.patt.search(response.text):
            r = json.loads(response.text.split('</script>')[-1])
            data=r['data']
            for each in data:
                item=crawler116()
                item['punish_date']=each['CF_SXQ']
                item['entity_name']=each['CF_XDR_MC']
                item['case_no']=each['CF_WSH']
                item['source_url']='http://xyhn.hainan.gov.cn/JRBWeb/website/SysXymlResourcesEditController.do?reqCode=showxzxkxx&key=%27{}%27&stype=2'.format(each['uuid'])
                item['punish_agent']=each['CF_XZJG']
                item['org_code']=each['QYBM_ID']
                item['notice_id']=each['uuid']
                item['spider_name']=self.name
                yield scrapy.Request(item['source_url'],
                                     meta={'item': item},
                                     dont_filter=True,
                                     callback=self.parsePageDetail
                                     )
        else:
            print('=====================ip blocked========================')
            print(self.patt.search(response.text).group(1))
    def parsePageDetail(self,response):
        # print('======pageDetail======',response.text,'=========pageDetail===========')
        if not self.patt.search(response.text):
            r=json.loads(response.text)
            table_text=r.get('contentViewsMap').get('rightData1')
            soup = BeautifulSoup(table_text, 'lxml')
            if not soup.find('div',class_=re.compile(r'ip')):
                item=response.meta['item']
                item['punish_reason']=soup.find_all('tr')[5].find_all('td')[-1].get_text(strip=True).replace(' ','').replace('\t','').replace('\n','').replace('\r','')
                item['punish_type1']=soup.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
                item['source_page']=response.text
                yield item
            else:
                print('=====================ip blocked========================')
                print(self.patt.search(response.text).group(1))
        else:
            print('=====================ip blocked========================')
            print(self.patt.search(response.text).group(1))
