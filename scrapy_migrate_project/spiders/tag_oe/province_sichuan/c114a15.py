# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_migrate_project.items import crawler114
from bs4 import BeautifulSoup
import requests
import re
import time
class C114a15inSpider(scrapy.Spider):
    """四川经营异常名录列入"""
    name = 'c114a15in'
    allowed_domains = ['sc.gsxt.gov.cn']
    url='http://sc.gsxt.gov.cn/notice/search/GET/announce?type=0101&mode=all&pageNo={}&areaId=&keyword='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Host': 'sc.gsxt.gov.cn',
        'Referer': 'http://hn.gsxt.gov.cn/notice/search/ent_announce',
        'Connection':'max-age=0',
        'X-Requested-With':'XMLHttpRequest'
        }
    def start_requests(self):
        # url=self.url.format(1)
        # r=requests.get(url,headers=self.headers)
        # print('------------requests-------------',r.text)
        yield scrapy.Request(self.url.format(1),
                             headers=self.headers,
                             )

    def parse(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        if not soup.find('div', class_=re.compile(u'ip')):
            r=json.loads(response.text.split('</script>')[-1])
            # print('======================',type(r),'=========================')
            totalpages=r.get('result').get('pageCount')
            print(totalpages,type(totalpages))
            for page in range(1,1+totalpages):
                yield scrapy.Request(self.url.format(page),
                                     dont_filter=True,
                                     callback=self.parseJson)
        else:
            print('=====================ip blocked========================')
            print(soup.find('div', class_=re.compile(u'ip')).get_text(strip=True))
    def parseJson(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        if not soup.find('div', class_=re.compile(u'ip')):
            r = json.loads(response.text.split('</script>')[-1])
            data=r['result']['data']
            for each in data:
                item=crawler114()
                item['spider_name']=item['data_source']=self.name
                item['punish_date']=each['date']
                item['entity_name']=each['etpName']
                item['source_url']='http://sc.gsxt.gov.cn/notice/'+each['link']
                item['punish_agent']=each['orgName']
                item['notice_id']=each['link'].split('uuid=')[-1].split('&')[0]
                yield scrapy.Request(item['source_url'],
                                     meta={'item': item},
                                     dont_filter=True,
                                     callback=self.parsePageDetail
                                     )
        else:
            print('=====================ip blocked========================')
            print(soup.find('div', class_=re.compile(r'ip')).get_text(strip=True))
    def parsePageDetail(self,response):
        # print('======pageDetail======',response.text,'=========pageDetail===========')
        soup=BeautifulSoup(response.text,'lxml')
        if not soup.find('div',class_=re.compile(r'ip')):
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
            item['source_page'] = response.text
            item['reg_no'] = ''
            item['report_year'] = ''
            # item['spider_name'] = ''
            # item['notice_id'] = ''
            item['punish_reason']=soup.find_all('div',class_='jjyc_word')[0].get_text(strip=True).replace(' ','').replace('\t','').replace('\n','').replace('\r','')
            item['case_no']=soup.find_all('div',class_='jjyc_word')[0].p.get_text(strip=True)
            yield item
        else:
            print('=====================ip blocked========================',soup.find('div', class_=re.compile(r'ip')).get_text(strip=True))


class C114a15outSpider(scrapy.Spider):
    """四川经营异常名录qianchu"""
    name = 'c114a15out'
    allowed_domains = ['sc.gsxt.gov.cn']
    url='http://sc.gsxt.gov.cn/notice/search/GET/announce?type=0102&mode=all&pageNo={}&areaId=&keyword='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Host': 'sc.gsxt.gov.cn',
        'Referer': 'http://hn.gsxt.gov.cn/notice/search/ent_announce',
        'Connection':'max-age=0',
        'X-Requested-With':'XMLHttpRequest'
        }
    def start_requests(self):
        # url=self.url.format(1)
        # r=requests.get(url,headers=self.headers)
        # print('------------requests-------------',r.text)
        yield scrapy.Request(self.url.format(1),
                             headers=self.headers,
                             )

    def parse(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        if not soup.find('div', class_=re.compile(u'ip')):
            r=json.loads(response.text.split('</script>')[-1])
            # print('======================',type(r),'=========================')
            totalpages=r.get('result').get('pageCount')
            print(totalpages,type(totalpages))
            for page in range(1,1+totalpages):
                yield scrapy.Request(self.url.format(page),
                                     dont_filter=True,
                                     callback=self.parseJson)
        else:
            print('=====================ip blocked========================')
            print(soup.find('div', class_=re.compile(u'ip')).get_text(strip=True))
    def parseJson(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        if not soup.find('div', class_=re.compile(u'ip')):
            r = json.loads(response.text.split('</script>')[-1])
            data=r['result']['data']
            for each in data:
                item=crawler114()
                item['spider_name']=item['data_source']=self.name
                item['release_date']=each['date']
                item['entity_name']=each['etpName']
                item['source_url']='http://sc.gsxt.gov.cn/notice/'+each['link']
                item['release_org']=each['orgName']
                item['data_id']=each['link'].split('uuid=')[-1].split('&')[0]
                yield scrapy.Request(item['source_url'],
                                     meta={'item': item},
                                     dont_filter=True,
                                     callback=self.parsePageDetail
                                     )
        else:
            print('=====================ip blocked========================')
            print(soup.find('div', class_=re.compile(r'ip')).get_text(strip=True))
    def parsePageDetail(self,response):
        # print('======pageDetail======',response.text,'=========pageDetail===========')
        soup=BeautifulSoup(response.text,'lxml')
        if not soup.find('div',class_=re.compile(r'ip')):
            item=response.meta['item']
            # item['case_no'] = ''
            # item['release_org'] = ''
            # item['release_date'] = ''
            # item['entity_name'] = ''
            # item['release_reason'] = ''
            # item['data_id'] = ''
            # item['data_source'] = self.name
            item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
            # item['source_url'] = ''
            # item['source_page'] = ''
            item['reg_no'] = ''
            # item['spider_name'] = ''
            item['source_page']=response.text
            item['release_reason']=soup.find_all('div',class_='jjyc_word')[0].get_text(strip=True).replace(' ','').replace('\t','').replace('\n','').replace('\r','')
            item['case_no']=soup.find_all('div',class_='jjyc_word')[0].p.get_text(strip=True)
            yield item
        else:
            print('=====================ip blocked========================',soup.find('div', class_=re.compile(r'ip')).get_text(strip=True))

