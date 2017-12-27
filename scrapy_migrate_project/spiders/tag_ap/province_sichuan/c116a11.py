# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_migrate_project.items import crawler116
from bs4 import BeautifulSoup
import requests
import re
import time
class C116a11Spider(scrapy.Spider):
    name = 'c116a11'
    allowed_domains = ['www.cdcredit.gov.cn']
    url='https://www.cdcredit.gov.cn/homePage/findDoublePubList.do'
    # headers = {
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    #     'Host': 'xyhn.hainan.gov.cn',
    #     'Referer': 'http://hn.gsxt.gov.cn/notice/search/ent_announce',
    #     'Connection':'keep-alive',
    #     'X-Requested-With':'XMLHttpRequest'
    #     }
    formdata={
        'dataType': '0',
        'pageSize': '10',
       'page': '1',
        'keyWord':'',
        'appType':'APP001'
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
            r=json.loads(response.text.split('</script>')[-1])
            # print('======================',r,'=========================')
            pagesize=10
            # print(r)
            total=r['msg'].get('total')
            totalpages=total//pagesize if total%pagesize==0 else total//pagesize+1
            print(totalpages,type(totalpages))

            for page in range(1,1+totalpages):
                self.formdata['page'] = str(page)
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
            data=r['msg']['rows']
            for data in data:
                item=crawler116()
                item['spider_name']=self.name
                item['punish_reason'] = data['fullname']
                item['notice_id'] = data['id']

                data={'id':data['id'],
                      'dataType':'0',
                      'appType':'APP001'}
                url='https://www.cdcredit.gov.cn/homePage/findDoublePubDetail.do'
                yield scrapy.FormRequest(url,
                                    formdata=data,
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
            # print('====================',r)
            data=r.get('msg').get('items')
            item = response.meta['item']
            item['case_no'] = data[1].get('value')

            item['credit_no'] =data[7].get('value')
            item['org_code'] = data[8].get('value')
            item['reg_no'] = data[9].get('value')
            item['tax_no'] = data[10].get('value')
            item['identity_card'] =data[11].get('value')

            item['current_status'] = data[16].get('value')
            item['area_code'] = data[17].get('value')
            item['offical_updtime'] = data[18].get('value')
            item['note'] = data[19].get('value')
            item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
            item['update_date'] = ''
            item['punish_type2'] = data[5].get('value')
            item['entity_type'] = ''
            item['data_source'] = self.name
            item['source_url'] = ''

            item['punish_date']=data[14].get('value')
            item['entity_name']=data[6].get('value')
            item['punish_agent']=data[15].get('value')

            item['punish_type1'] =data[4].get('value')
            item['legal_man']=data[12].get('value')
            item['punish_result']=data[13].get('value')
            item['law_item']=data[3].get('value')
            item['source_page']=response.text
            yield item
        else:
            print('=====================ip blocked========================')
            print(self.patt.search(response.text).group(1))
