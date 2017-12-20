# -*- coding: utf-8 -*-
import re

import requests
import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler116


class Crawler1166Spider(scrapy.Spider):
    name = 'crawler116_6'
    allowed_domains = ['www.gdcredit.gov.cn']

    def start_requests(self):
        url_page = 'http://www.gdcredit.gov.cn/infoTypeAction!xzTwoPublicList.do?type=7&depType=0'
        html = requests.get(url_page)
        total_page_ = re.findall('id="totalPage" value="(.*?)"', html.text, re.S)[0]
        total_page = int(total_page_)

        for i in range(1,total_page):
            url = 'http://www.gdcredit.gov.cn/infoTypeAction!xzTwoPublicList.do?type=7&depType=0'
            yield scrapy.FormRequest(url=url,formdata={"type":"7","depType":"0","page":str(i),"pageSize":"10"})


    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content,"lxml")
        tags_td = soup.find_all(class_="xzxx-first")
        for each in tags_td:
            detail_url_ = each.find_all('a')[0]['href']
            detail_url = 'http://www.gdcredit.gov.cn' + detail_url_

            yield scrapy.Request(url=detail_url,callback=self.parse_detail)


    def parse_detail(self,response):
        item = crawler116()
        content_all = response.body
        list = []
        content1 = re.findall('<div class="data">(.*?)<div class="pageFragment_bg_down"></div>', content_all, re.S)[0]
        content = re.findall('<td class="value">(.*?)</td>', content1, re.S)
        for each in content:
            each = each.replace('\t', '').replace(' ', '').replace('\r\n', '')
            list.append(each)
        no_field1 = re.findall('<td class="value table-inner">(.*?)</table>', content1, re.S)[0]
        no_field = re.findall('<tr class="value">(.*?)</tr>', no_field1, re.S)[0]
        no1 = re.findall('<td class="left">(.*?)</td>', no_field, re.S)[0].replace('\t', '').replace(' ', '').replace(
            '\r\n', '')
        list.append(no1)
        no2 = re.findall('<td>(.*?)</td>', no_field, re.S)
        no3 = re.findall('<td class="right">(.*?)</td>', no_field, re.S)[0].replace('\t', '').replace(' ', '').replace(
            '\r\n', '')
        list.append(no3)
        for each in no2:
            each = each.replace('\t', '').replace(' ', '').replace('\r\n', '')
            list.append(each)
        no4 = re.findall('<td >(.*?)</td>', no_field, re.S)[0]
        list.append(no4)

        create_date = time.strftime('%Y-%m-%d', time.localtime())

        case_no = list[0]
        punish_type1 = list[2]
        punish_type2 = list[3]
        punish_reason = list[4]
        law_item = list[5]
        entity_name = list[7]
        credit_no = list[15]
        org_code = list[17]
        reg_no = list[18]
        tax_no = list[19]
        identity_card = list[16]
        legal_man = list[8]
        punish_result = list[6]
        punish_date = list[9]
        punish_agent = list[10]
        current_status = list[12]
        area_code = list[11]
        offical_updtime = list[13]
        note = list[14]
        create_date = create_date
        update_date = ''
        entity_type = '2'
        data_source = '6'

        item['case_no'] =case_no
        item['punish_type1'] =punish_type1
        item['punish_type2'] =punish_type2
        item['punish_reason'] =punish_reason
        item['law_item'] =law_item
        item['entity_name'] =entity_name
        item['credit_no'] =credit_no
        item['org_code'] =org_code
        item['reg_no'] =reg_no
        item['tax_no'] = tax_no
        item['identity_card'] =identity_card
        item['legal_man'] =legal_man
        item['punish_result'] =punish_result
        item['punish_date'] =punish_date
        item['punish_agent'] =punish_agent
        item['current_status'] =current_status
        item['area_code'] =area_code
        item['offical_updtime'] =offical_updtime
        item['note'] =note
        item['create_date'] = create_date
        # item['update_date'] =update_date
        item['entity_type'] = entity_type
        item['data_source'] = data_source
        item['source_url'] = response.url
        item['source_page'] = content
        item['spider_name']=self.name


        yield item



