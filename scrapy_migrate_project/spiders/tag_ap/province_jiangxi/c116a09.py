# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_migrate_project.items import crawler116
from bs4 import BeautifulSoup
import requests
import re
import time
class C116a09Spider(scrapy.Spider):
    name = 'c116a09'
    allowed_domains = ['www.creditjx.gov.cn']
    url='http://www.creditjx.gov.cn/datareporting/doublePublicity/queryDoublePublicityList.json'

    formdata={
            'tableType':'1',
            'inpParam':'',
            'orgIdOrRegionId':'',
            'page':'1',
            'pageSize':'15'
            }
    patt = re.compile(r'\d+\.\d+\.\d+\.\d+')
    def start_requests(self):

        yield scrapy.FormRequest(self.url,
                                 formdata=self.formdata
                             # headers=self.headers,
                             )

    def parse(self, response):
        if not self.patt.search(response.text):
            r=json.loads(response.text.split('</script>')[-1])
            # print('======================',r,'=========================')

            totalpages=r.get('pageCount')
            # print(totalpages,type(totalpages))

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
        if not self.patt.search(response.text):
            r = json.loads(response.text.split('</script>')[-1])
            data=r['list']
            for each in data:
                item=crawler116()
                item['credit_no'] =each['creditCode']
                item['reg_no'] = ''
                item['identity_card'] =each['idCard']
                item['current_status'] = ''
                item['area_code'] = each['areaCode']
                item['offical_updtime'] = each['uploadTime']
                item['note'] = ''
                item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
                item['update_date'] = ''
                item['punish_type2'] = each['punishTypeTwo']
                item['entity_type'] = each['organizationCode']
                item['data_source'] = response.text
                item['spider_name']=self.name
                item['tax_no']=each['taxCode']
                item['punish_date']=each['punishDate']
                item['entity_name']=each['personName']
                item['case_no']=each['punishNumber']
                item['punish_reason'] = each['punishReason']
                item['source_url']='http://www.creditjx.gov.cn/datareporting/doublePublicity/punishDetail/{}'.format(each['id'])
                item['punish_agent']=each['punishState']
                item['org_code']=each['orgId']
                item['notice_id']=each['id']
                item['punish_type1'] =each['punishTypeOne']
                item['legal_man']=each['legalName']
                item['punish_result']=each['punishResult']
                item['law_item']=each['punishBy']
                item['source_page']=response.text
                yield item
        else:
            print('=====================ip blocked========================')
            print(self.patt.search(response.text).group(1))

