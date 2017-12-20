# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
import json
from scrapy_migrate_project.items import C009Item

class C009Spider(scrapy.Spider):
    name = 'c009'
    allowed_domains = ['jzsc.mohurd.gov.cn']
    url = 'http://jzsc.mohurd.gov.cn/asite/credit/record/query'
    # formdata={'$total': '', '$reload': '0', '$pg': '1', '$pgsz': '10'}
    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        patt=re.compile(r'__pgfm\(\'\'\,(\{.*?\})')
        self.formdata=json.loads(patt.search(response.text).group(1))
        pages=self.formdata['$total']/10 if self.formdata['$total']%10==0 else int(self.formdata['$total']/10)+1
        for page in range(1,1+pages):
            self.formdata['$pg']=str(page)
            for key in self.formdata.keys():
                self.formdata[key]=str(self.formdata[key])
            print(self.formdata)
            yield scrapy.FormRequest(self.url,
                                     formdata=self.formdata,
                                     dont_filter=True,
                                     callback=self.parsePageDetail)
    def parsePageDetail(self,response):
        soup= BeautifulSoup(response.text,'lxml')
        trs=soup.tbody.find_all('tr')
        patt=re.compile(r'(\d.*\d)')
        for each in trs:
            item=C009Item()
            # item['source_page']=each
            item['spider_name'] = self.name
            item['credit_icon'] = each.find_all('td')[0].a.get_text(strip=True)
            item['credit_recordNum'] = each.find_all('td')[0].span.get_text(strip=True)
            item['credit_recordBody'] = each.find_all('td')[1].get_text(strip=True)

            item['credit_recordBodyTag'] = each.find_all('td')[2].span.get_text(strip=True)

            item['reason'] = each.find_all('td')[2].a.attrs['data-text']
            item['resultTag'] = each.find_all('td')[2].span.get_text(strip=True)[1:-1]
            each.find_all('td')[2].span.extract()
            if each.find_all('td')[2].span.get_text(strip=True):
                if patt.search(each.find_all('td')[2].span.get_text(strip=True)):
                    item['recordTime'] = patt.search(each.find_all('td')[2].span.get_text(strip=True)).group(1)
            #     else:
            #         print('---------------------------------------', each.find_all('td')[2].span.get_text(strip=True))
            # else:
            #     print('---------------------------------------',each.find_all('td')[2].span)

            each.find_all('td')[2].div.extract()
            item['result'] = each.find_all('td')[2].get_text(strip=True)


            item['notice_id'] = each.find_all('td')[3].div.get_text(strip=True)
            each.find_all('td')[3].div.extract()
            item['administration'] =each.find_all('td')[3].get_text(strip=True)
            if each.find_all('td')[1].a:
                item['credit_recordBodyDetailUrl'] ='http://jzsc.mohurd.gov.cn'+ each.find_all('td')[1].a.attrs['href']

                yield scrapy.Request(item['credit_recordBodyDetailUrl'],
                                 meta={'item':item},
                                 dont_filter=True,
                                 callback=self.parse_bodyDetail
                                 )
            else:
                yield item



    def parse_bodyDetail(self,response):
        item=response.meta['item']
        # item['source_page'] = response.text
        item['source_url']=response.url


        if 'staff' in item['credit_recordBodyDetailUrl']:
            soup=BeautifulSoup(response.text,'lxml')
            soup.find('dd', class_="query_info_dd1").span.extract()

            item['credit_recordBodyGender'] = soup.find('dd',class_="query_info_dd1").get_text(strip=True)
            soup.find_all('dd', class_="query_info_dd2")[-1].span.extract()
            item['credit_recordBodyID'] = soup.find_all('dd', class_="query_info_dd2")[-1].get_text(strip=True)

        yield item
