# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from scrapy_migrate_project.items import C012Item
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
            item = C012Item()
            item['spider_name']=self.name
            item['company_name']=each.find_all('td')[0].get_text(strip=True)
            item['notice_id']=re.search(r"Detail\(\'(\w+)\'",each.find_all('td')[0].a.attrs['onclick']).group(1)
            item['company_detail_pageUrl']='http://www.tjcredit.gov.cn/gsxt/excdir/detail?id='+item['notice_id']
            item['administration']=each.find_all('td')[1].get_text(strip=True)
            item['why_listed_in']=each.find_all('td')[2].get_text(strip=True)
            item['annals_year']=each.find_all('td')[3].get_text(strip=True)
            item['year_listed_in']=each.find_all('td')[4].get_text(strip=True)
            item['create_date']= time.strftime('%Y-%m-%d', time.localtime())
            item['source_page']=str(each).replace(' ','').replace('\t','').replace('\n','').replace('\r','')


            yield item


