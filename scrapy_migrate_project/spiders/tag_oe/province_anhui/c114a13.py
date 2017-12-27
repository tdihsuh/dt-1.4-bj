# -*- coding: utf-8 -*-
"""
弹验证码，封ip

"""
import scrapy
from bs4 import BeautifulSoup
import re
from scrapy_migrate_project.items import crawler114,crawler114_out
import time

class C114a13inSpider(scrapy.Spider):
    """安徽经营异常名录列入"""
    name = 'c114a13in'
    allowed_domains = ['ah.gsxt.gov.cn/infoAnnoucement.jspx']
    url='http://ah.gsxt.gov.cn/ycmlNoticeInfo.jspx?mark=01&pageNo={}&order=2&title=&area='
    def start_requests(self):
        yield scrapy.Request(self.url.format(1))

    def parse(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        patt=re.compile(u'(\d+)')
        pagestring=soup.find('div').find_all('li')[1].get_text(strip=True)
        # print(pagestring)
        total=patt.search(pagestring).group(1)
        # print(total)
        totalpages=int(total)
        for page in range(1,1+totalpages):
            yield scrapy.Request(self.url.format(page),
                                 callback=self.parseDetail,
                                 dont_filter=True)
    def parseDetail(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        trs=soup.find_all('tr')
        for each in trs:
            item=crawler114()
            if each.find_all('td')[2].get_text(strip=True):
                item['punish_agent'] = each.find_all('td')[2].get_text(strip=True)
            item['punish_date'] = each.find_all('td')[3].get_text(strip=True)
            item['spider_name']=item['data_source']=self.name
            if each.find_all('td')[1].a:
                item['notice_id'] = each.find_all('td')[1].a.attrs['href'].split('id=')[-1]
                item['entity_name'] = each.find_all('td')[1].get_text(strip=True).replace(u'关于', '').replace(u'列入经营异常名录公告', '')
                item['source_url'] = 'http://ah.gsxt.gov.cn'+each.find_all('td')[1].a.attrs['href']
                yield scrapy.Request(item['source_url'],
                                     meta={'item': item},
                                     dont_filter=True,
                                     callback=self.parsePageDetail
                                     )


    def parsePageDetail(self,response):
        soup=BeautifulSoup(response.text,'lxml')
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
        item['source_page']=response.text
        item['punish_reason']=soup.find('div',class_='Section1').get_text(strip=True).replace(' ','').replace('\t','').replace('\n','').replace('\r','')
        item['case_no']=soup.find('div',class_='Section1').find_all('p',align='center')[-1].get_text(strip=True)
        yield item
class C114a13outSpider(scrapy.Spider):
    """安徽经营异常名录迁出"""
    name = 'c114a13out'
    allowed_domains = ['ah.gsxt.gov.cn/infoAnnoucement.jspx']
    url='http://ah.gsxt.gov.cn/ycmlNoticeInfo.jspx?mark=02&pageNo={}&order=2&title=&area='
    def start_requests(self):
        yield scrapy.Request(self.url.format(1))

    def parse(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        patt=re.compile(u'(\d+)')
        pagestring=soup.find('div').find_all('li')[1].get_text(strip=True)
        print(pagestring)
        total=patt.search(pagestring).group(1)
        print(total)
        totalpages=int(total)
        for page in range(1,1+totalpages):
            yield scrapy.Request(self.url.format(page),
                                 callback=self.parseDetail,
                                 dont_filter=True)
    def parseDetail(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        trs=soup.find_all('tr')
        for each in trs:
            item=crawler114_out()
            if each.find_all('td')[2].get_text(strip=True):
                item['release_org'] = each.find_all('td')[2].get_text(strip=True)
            else:
                item['release_org']=''
            item['release_date'] = each.find_all('td')[3].get_text(strip=True)
            item['spider_name']=item['data_source']=self.name
            if each.find_all('td')[1].a:
                item['data_id'] = each.find_all('td')[1].a.attrs['href'].split('id=')[-1]
                item['entity_name'] = each.find_all('td')[1].get_text(strip=True).replace(u'关于', '').replace(u'列入经营异常名录公告', '')
                item['source_url'] = 'http://ah.gsxt.gov.cn'+each.find_all('td')[1].a.attrs['href']
                yield scrapy.Request(item['source_url'],
                                     meta={'item': item},
                                     dont_filter=True,
                                     callback=self.parsePageDetail
                                     )


    def parsePageDetail(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        item=response.meta['item']
        # item['case_no'] = ''
        # item['release_org'] = ''
        # item['release_date'] = ''
        # item['entity_name'] = ''
        # item['release_reason'] = ''
        # item['data_id'] = ''
        item['data_source'] = self.name
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        # item['source_url'] = ''
        # item['source_page'] = ''
        item['reg_no'] = ''
        # item['spider_name'] = ''
        item['source_page']=response.text
        item['release_reason']=soup.find('div',class_='Section1').get_text(strip=True).replace(' ','').replace('\t','').replace('\n','').replace('\r','')
        item['case_no']=soup.find('div',class_='Section1').find_all('p',align='center')[-1].get_text(strip=True)
        yield item


