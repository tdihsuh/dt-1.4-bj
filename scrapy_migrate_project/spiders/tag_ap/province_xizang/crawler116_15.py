# -*- coding: utf-8 -*-
# 信用中国（西藏）
import re,sys

from bs4 import BeautifulSoup
from scrapy_migrate_project.items import crawler116
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy


class Xz015Spider(scrapy.Spider):
    name = 'crawler116_15'
    allowed_domains = ['creditxizang.gov.cn']
    url = 'http://www.creditxizang.gov.cn/xyxz/doublePublicController/toDoublePublicPage?keyword='
    formdata = {
        'pageNum': '1',
        'numPerPage': '10',
        'orderField': '',
        'orderDirection': '',
        'prePage': '1',
        'nextPage': '2',
        'ttPage': '7'
    }
    patt = re.compile(r'\d+\.\d+\.\d+\.\d+')

    def start_requests(self):
        yield scrapy.FormRequest(self.url,
                                 formdata=self.formdata
                                 )

    def parse(self, response):
        if not self.patt.search(response.text):
            data =  response.text
            totalpages = re.findall(u'共有(\d+)页', data)[0]
            
            totalpages = int(totalpages)
            for page in range(1, totalpages+1):
                self.formdata['page'] = str(page)
                yield scrapy.FormRequest(self.url,
                                         formdata= {
                                                    'pageNum': str(page),
                                                    'numPerPage': '10',
                                                    'orderField': '',
                                                    'orderDirection': '',
                                                    'prePage': '4',
                                                    'nextPage': '6',
                                                    'ttPage': '7'
                                                },
                                         dont_filter=True,
                                         callback=self.parseDetail)


    def parseDetail(self, response):
        if not self.patt.search(response.text):
            soup = BeautifulSoup(response.text, 'lxml')
            trs = soup.find('div', id='content').find_all('tr')
            for data in trs[1:]:
                item = crawler116()
                item['entity_name'] = data.find_all('td')[2].get_text(strip=True)
                item['source_url'] = 'http://www.creditxizang.gov.cn' + data.find_all('td')[1].a['href']
                item['case_no'] = data.find_all('td')[0].get_text(strip=True)
                item['punish_agent'] = data.find_all('td')[3].get_text(strip=True)
                url = response.url
                item['source_url'] = url
                item['spider_name'] = self.name
                data = response.text
                item['source_page'] = data
                yield item