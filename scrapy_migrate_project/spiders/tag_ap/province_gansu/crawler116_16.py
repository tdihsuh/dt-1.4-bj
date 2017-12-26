# -*- coding: utf-8 -*-
# 信用甘肃
import re
from scrapy_migrate_project.items import crawler116
import scrapy
from bs4 import BeautifulSoup


class Gs016Spider(scrapy.Spider):
    name = 'crawler116_16'
    allowed_domains = ['gscredit.gov.cn']
    url = 'http://www.gscredit.gov.cn/sgs/xzcf/list_{}.jspx?type={}'
    patt = re.compile(r'\d+\.\d+\.\d+\.\d+')

    def start_requests(self):
        for i in range(1, 6):  # 一共就5页
            for j in ['legal', 'person']:
                yield scrapy.FormRequest(self.url.format(i, j), dont_filter=True)

    def parse(self, response):
        if not self.patt.search(response.text):
            soup = BeautifulSoup(response.text, 'lxml')
            ul = soup.find_all('ul', id='search-result-list')[0]
            for li in ul.find_all('li'):
                if 'legal' in response.url:
                    yield scrapy.Request('http://www.gscredit.gov.cn' + li.a.attrs['href'],
                                         callback=self.parseLegal,
                                         dont_filter=True)
                else:
                    yield scrapy.Request('http://www.gscredit.gov.cn' + li.a.attrs['href'],
                                         callback=self.parsePerson,
                                         dont_filter=True)

    def parseLegal(self, response):
        if not self.patt.search(response.text):
            soup = BeautifulSoup(response.text, 'lxml')
            data = soup.find('ul', class_=re.compile(r'new-tab1')).find_all('li')
            item = crawler116()
            item['entity_name'] = data[5].find_all('p')[-1].get_text(strip=True)

            item['credit_no'] = data[6].find_all('p')[-1].get_text(strip=True)

            item['punish_type1'] = data[2].find_all('p')[-1].get_text(strip=True)
            item['case_no'] = data[0].find_all('p')[-1].get_text(strip=True)
            item['legal_man'] = data[11].find_all('p')[-1].get_text(strip=True)
            item['punish_agent'] = data[15].find_all('p')[-1].get_text(strip=True)
            item['law_item'] = data[4].find_all('p')[-1].get_text(strip=True)
            item['punish_result'] = data[12].find_all('p')[-1].get_text(strip=True)
            item['punish_reason'] = data[3].find_all('p')[-1].get_text(strip=True)
            item['notice_id'] = response.url.split('id=')[-1]
            item['punish_date'] = data[13].find_all('p')[-1].get_text(strip=True)
            url = response.url
            item['source_url'] = url
            item['spider_name'] = self.name
            data = response.text
            item['source_page'] = data
            item['reg_no'] = ''
            item['tax_no'] = ''
            item['identity_card'] = ''
            item['org_code'] = ''
            item['current_status'] = ''
            item['area_code'] = ''
            item['offical_updtime'] = ''
            item['note'] = ''
            item['create_date'] = ''
            item['update_date'] = ''
            item['punish_type2'] = ''
            item['entity_type'] = ''
            item['data_source'] = ''
            yield item

    def parsePerson(self, response):
        if not self.patt.search(response.text):
            soup = BeautifulSoup(response.text, 'lxml')
            data = soup.find('ul', class_=re.compile(r'new-tab1')).find_all('li')

            item = crawler116()
            item['entity_name'] = data[5].find_all('p')[-1].get_text(strip=True)
            item['identity_card'] = data[6].find_all('p')[-1].get_text(strip=True)
            # item['case_name'] = data[1].find_all('p')[-1].get_text(strip=True)
            item['punish_type1'] = data[2].find_all('p')[-1].get_text(strip=True)
            item['case_no'] = data[0].find_all('p')[-1].get_text(strip=True)

            item['punish_agent'] = data[9].find_all('p')[-1].get_text(strip=True)
            item['law_item'] = data[4].find_all('p')[-1].get_text(strip=True)
            item['punish_result'] = data[7].find_all('p')[-1].get_text(strip=True)
            item['punish_reason'] = data[3].find_all('p')[-1].get_text(strip=True)
            item['notice_id'] = response.url.split('id=')[-1]
            item['punish_date'] = data[8].find_all('p')[-1].get_text(strip=True)
            url = response.url
            item['source_url'] = url
            item['spider_name'] = self.name
            data = response.text
            item['source_page'] = data
            item['reg_no'] = ''
            item['tax_no'] = ''
            item['legal_man'] = ''
            item['credit_no'] = ''
            item['org_code'] = ''
            item['current_status'] = ''
            item['area_code'] = ''
            item['offical_updtime'] = ''
            item['note'] = ''
            item['create_date'] = ''
            item['update_date'] = ''
            item['punish_type2'] = ''
            item['entity_type'] = ''
            item['data_source'] = ''
            yield item


