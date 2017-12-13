# -*- coding: utf-8 -*-
import re

import requests
import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler116


class Crawler1161Spider(scrapy.Spider):
    name = 'crawler116_1'
    allowed_domains = ['58.42.237.143']

    def start_requests(self):
        url_page = 'http://58.42.237.143:8080/gs/gdsgs/xzcfxx/list'
        page_num = requests.get(url_page)
        page_num_field = re.findall('<div class="pages">(.*?)</div>', page_num.text, re.S)[0]
        total_page_ = re.findall('<strong>(.*?)</strong>', page_num_field, re.S)[0]
        total_page = int(total_page_)

        for i in range(1,total_page+1):
            url = 'http://58.42.237.143:8080/gs/gdsgs/xzcfxx/list'
            yield scrapy.FormRequest(url=url,formdata={"pageNo":str(i),"pageSize":"10"})



    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content,"lxml")
        tags_a = soup.find_all('a',class_="title")
        for each in tags_a:
            detail_url = 'http://58.42.237.143:8080'+each['href']

            yield scrapy.Request(url=detail_url,callback=self.parse_detail)


    def parse_detail(self,response):
        item = crawler116()
        content = response.body
        content_detail = []
        content_field = re.findall('class="table_normal1">(.*?)</table>', content, re.S)[0]
        content1 = re.findall('<td(.*?)</td>', content_field, re.S)
        for each in content1:
            each = each.replace('>', '').replace('\t', '').replace('\0', '').replace(' ', '').replace('\r\n',
                                                                                                      '').replace(
                '&yen;', '')
            content_detail.append(each)

        create_date = time.strftime('%Y-%m-%d', time.localtime())
        credit_no = content_detail[6]
        case_no = content_detail[0]
        punish_type1 = content_detail[2]
        punish_reason = content_detail[3]
        law_item = content_detail[4]
        entity_name = content_detail[5]
        org_code = content_detail[7]
        reg_no = content_detail[8]
        tax_no = content_detail[9]
        identity_card = content_detail[10]
        legal_man = content_detail[11]
        punish_result = content_detail[12]
        punish_date = content_detail[13]
        punish_agent = content_detail[15]
        current_status = content_detail[16]
        area_code = content_detail[17]
        offical_updtime = content_detail[18]
        note = content_detail[19]
        create_date = create_date
        update_date = ''
        punish_type2 = ''
        entity_type = '0'
        data_source = '1'

        item['credit_no'] =credit_no
        item['case_no'] =case_no
        item['punish_type1'] =punish_type1
        item['punish_reason'] =punish_reason
        item['law_item'] =law_item
        item['entity_name'] =entity_name
        item['org_code'] =org_code
        item['reg_no'] =reg_no
        item['tax_no'] =tax_no
        item['identity_card'] = identity_card
        item['legal_man'] =legal_man
        item['punish_result'] =punish_result
        item['punish_date'] =punish_date
        item['punish_agent'] =punish_agent
        item['current_status'] =current_status
        item['area_code'] =area_code
        item['offical_updtime'] =offical_updtime
        item['note'] =note
        item['create_date'] =create_date
        item['update_date'] = update_date
        item['punish_type2'] =punish_type2
        item['entity_type'] =entity_type
        item['data_source'] =data_source
        item['source_url'] = response.url
        item['source_page'] = content

        yield item




