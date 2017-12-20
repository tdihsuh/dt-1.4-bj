"""
http://www.credithebei.gov.cn/
http://123.182.226.146:8082/was5/web/detail?record=42276&channelid=284249
"""
# -*- coding: utf-8 -*-
import scrapy
import json
import time
from scrapy_migrate_project.items import crawler116
from bs4 import BeautifulSoup

class C011Spider(scrapy.Spider):
    name = 'c011'
    allowed_domains = ['*']
    url = 'http://123.182.226.146:8082/was5/web/detail?record={}&channelid=284249'

    def start_requests(self):
        totalpages=42276
        for page in range(1,totalpages+1):
            yield scrapy.Request(self.url.format(page),
                                 dont_filter=True,
                                 )

    def parse(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        trs=soup.table.find_all('tr')


        item = crawler116()
        item['case_no'] =  trs[0].find_all('td')[-1].get_text(strip=True)
        item['credit_no'] =trs[1].find_all('td')[-1].get_text(strip=True)
        item['punish_type1'] =trs[3].find_all('td')[-1].get_text(strip=True)
        item['punish_reason'] =trs[4].find_all('td')[-1].get_text(strip=True)
        item['law_item'] = trs[5].find_all('td')[-1].get_text(strip=True).replace(' ','').replace('\t','').replace('\n','').replace('\r','')
        item['entity_name'] =trs[6].find_all('td')[-1].get_text(strip=True)
        item['legal_man'] =trs[11].find_all('td')[-1].get_text(strip=True)
        item['punish_date']=trs[12].find_all('td')[-1].get_text(strip=True)
        # item['punishresult'] = .replace(' ','').replace('\t','').replace('\n','').replace('\r','')
        # item['timeresult'] = time.strftime('%Y-%m-%d', time.localtime(detaildic[jj]['f15'] / 1000))
        item['punish_agent'] =trs[13].find_all('td')[-1].get_text(strip=True)
        item['source_url']=response.url
        item['source_page']=response.text
        item['spider_name']=self.name
        yield item