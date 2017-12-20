# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_migrate_project.items import crawler116
from bs4 import BeautifulSoup
import requests
import re

class C116a10Spider(scrapy.Spider):
    name = 'c116a10'
    allowed_domains = ['www.creditsc.gov.cn']
    url='http://www.creditsc.gov.cn/SCMH/doublePublicController/toDoublePublicPage?keyword='
    url_detail = ''
    # headers = {
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    #     'Host': 'xyhn.hainan.gov.cn',
    #     'Referer': 'http://hn.gsxt.gov.cn/notice/search/ent_announce',
    #     'Connection':'keep-alive',
    #     'X-Requested-With':'XMLHttpRequest'
    #     }
    formdata={
            'pageNum':'1',
            'numPerPage':'15',
            'orderField':'',
            'orderDirection':'',
            # 'prePage':'1',
            # 'nextPage':'3',
            'ttPage':'231',
            'totalCount':'3462',
            'count':'0'
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
            soup=BeautifulSoup(response.text,'lxml')
            totalpages= re.findall(u'totalPages: (\d+)\,',response.text, re.S)[0]
            totalCount=totalcount= re.findall(u'总共有(\d+)条',response.text, re.S)[0]
            # print('totalpages',type(totalpages),'totalCount',type(totalCount))
            self.formdata['ttPage'] = totalpages
            self.formdata['totalCount']=totalCount
            for page in range(1,1+int(totalpages)):
                self.formdata['pageNum']=str(page)

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
            soup=BeautifulSoup(response.text,'lxml')
            trs=soup.table.find_all('tr')
            for each in trs[1:]:
                item=crawler116()
                item['spider_name']=self.name
                item['case_no']=each.find_all('td')[0].a.attrs['title']
                item['entity_name'] =each.find_all('td')[2].a.attrs['title']
                item['punish_agent'] = each.find_all('td')[3].a.attrs['title']
                item['source_url']='http://www.creditsc.gov.cn'+each.find_all('td')[1].a.attrs['href']
                item['notice_id']=each.find_all('td')[1].a.attrs['href'].split('?')[-1]

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
            soup=BeautifulSoup(response.text,'lxml')
            # print('====================',r)
            lis=soup.find_all('ul')[-1].find_all('li')
            # print('###########    data    ############',lis)
            item = response.meta['item']
            item['punish_reason'] = lis[2].span.get_text(strip=True)
            # item['noticeid'] = data['VAL_ID']
            item['punish_date'] = lis[-5].span.get_text(strip=True)
            item['punish_type1'] =lis[4].span.get_text(strip=True)
            item['legal_man']=lis[-6].span.get_text(strip=True)
            item['punish_result']=lis[-3].span.get_text(strip=True)
            item['law_item']=lis[-3].span.get_text(strip=True)
            item['source_page']=response.text
            yield item
        else:
            print('=====================ip blocked========================')
            print(self.patt.search(response.text).group(1))
