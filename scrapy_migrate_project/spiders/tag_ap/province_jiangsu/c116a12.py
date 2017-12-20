# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_migrate_project.items import crawler116
from bs4 import BeautifulSoup
import requests
import re

class C116a12Spider(scrapy.Spider):
    name = 'c116a12'
    allowed_domains = ['wuxicredit.wuxi.gov.cn']
    url='http://wuxicredit.wuxi.gov.cn/intertidwebapp/cxIndex/getPContentByPage'
    url_detail = 'http://wuxicredit.wuxi.gov.cn/intertidwebapp/cxIndex/getPContentInfo'
    # headers = {
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    #     'Host': 'xyhn.hainan.gov.cn',
    #     'Referer': 'http://hn.gsxt.gov.cn/notice/search/ent_announce',
    #     'Connection':'keep-alive',
    #     'X-Requested-With':'XMLHttpRequest'
    #     }
    formdata={
        'type': '2',
        'pageSize': '10',
       'cpage': '1',
        'asc':'desc',
        'deptcode':'undefined',
        'orgbm':'undefined',
        'name':''
            }
    patt = re.compile(r'\d+\.\d+\.\d+\.\d+')
    def start_requests(self):
        # url=self.url.format(1,1)
        # r=requests.get(url,headers=self.headers)
        # print('------------requests-------------',r.text)
        yield scrapy.FormRequest(self.url,
                                 formdata=self.formdata
                             # headers=self.headers,
                             )

    def parse(self, response):
        if not self.patt.search(response.text):
            print(response.text)
            r=json.loads(response.text.split('</script>')[-1])
            print('======================',type(r),'=========================')
            pagesize=10
            # print(r)
            total=r.get('totalNum')
            totalpages=total//pagesize if total%pagesize==0 else total//pagesize+1
            print(totalpages,type(totalpages))

            for page in range(1,1+totalpages):
                self.formdata['cpage'] = str(page)
                yield scrapy.FormRequest(self.url,
                                         formdata=self.formdata,
                                     dont_filter=True,
                                     callback=self.parseJson)
        else:
            print('=====================ip blocked========================')
            print(self.patt.search(response.text).group(1))
    def parseJson(self,response):
        # patt=re.compile(r'\d+\.\d+\.\d+\.\d+')
        if not self.patt.search(response.text):
            r = json.loads(response.text.split('</script>')[-1])
            lists=r['mess']
            for data in lists:
                item=crawler116()
                item['entity_name'] =data['CF_XDR_MC']
                item['punish_agent'] = data['CF_XZJG']
                item['punish_reason'] = data['CF_CFMC']
                item['notice_id'] = data['VAL_ID']
                item['punish_date']=data['CF_JDRQ']
                item['spider_name']=self.name
                post_data={'valId':data['VAL_ID'],
                      'type':'2'}

                yield scrapy.FormRequest(self.url_detail,
                                         formdata=post_data,
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
            r = json.loads(response.text.split('</script>')[-1])
            # print('====================',r)
            data=r.get('mess')['detail']

            item = response.meta['item']

            item['case_no']=data['CF_WSH']

            item['punish_type1'] =data['CF_CFLB1']
            item['legal_man']=data['CF_FR']
            # item['punish_result']=data['CF_JG']
            item['law_item']=data['CF_YJ']
            # item['source_page']=response.text
            yield item
        else:
            print('=====================ip blocked========================')
            print(self.patt.search(response.text).group(1))
