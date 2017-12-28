# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from scrapy_migrate_project.items import crawler114
import time

class C012Spider(scrapy.Spider):
    name = 'c012'
    allowed_domains = ['www.tjcredit.gov.cn']
    url = 'http://www.tjcredit.gov.cn/gsxt/excdir/search'
    formdata={'pageIndex':'1',
            'pageSize':'10',
            'entname':''}
    def start_requests(self):

        yield scrapy.FormRequest(self.url,
                                 dont_filter=True,
                                 formdata=self.formdata,
                                 )

    def parse(self, response):
        soup=BeautifulSoup(response.text,'lxml')
        # print(soup)
        # stringPage=soup.find('script',src=None,type="text/javascript").get_text(strip=True)
        # print(stringPage)
        total=int(re.search(r'maxPage(.*?)(\d+)\;',response.text).group(2))
        print(total)
        pages= total/10 if total%10==0 else int(total/10)+1
        for page in range(1,1+pages):
            self.formdata['pageIndex']=str(page)
            yield scrapy.FormRequest(self.url,
                                     formdata=self.formdata,
                                     dont_filter=True,
                                     meta={'page':page},
                                     callback=self.parseDetail
                                     )
    def parseDetail(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        trs=soup.find('table',id='table').tbody.find_all('tr')

        for each in trs:
            item = crawler114()
            item['spider_name']=self.name
            item['entity_name']=each.find_all('td')[0].get_text(strip=True)
            item['notice_id']=re.search("Detail\(\'(\w+)\'",each.find_all('td')[0].a.attrs['onclick']).group(1)
            item['source_url']='http://www.tjcredit.gov.cn/gsxt/excdir/detail?id='+item['notice_id']
            item['punish_agent']=each.find_all('td')[1].get_text(strip=True)
            item['punish_reason']=each.find_all('td')[2].get_text(strip=True)
            item['punish_date']=each.find_all('td')[3].get_text(strip=True)
            item['report_year']=each.find_all('td')[4].get_text(strip=True)
            item['create_date']= time.strftime('%Y-%m-%d', time.localtime())
            item['source_page']=str(each).replace(' ','').replace('\t','').replace('\n', '').replace('\r','')
            item['data_id']=''
            item['data_source']=self.name
            item['del_flag']=''
            item['op_flag']=''
            item['case_no']=''
            item['reg_no']=''
            yield item


