# -*- coding: utf-8 -*-
import requests
import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler116


class Crawler1164Spider(scrapy.Spider):
    name = 'crawler116_4'
    allowed_domains = ['www.hbcredit.gov.cn']

    def start_requests(self):
        response = requests.get('http://www.hbcredit.gov.cn/credithb/gkgs/list.html?type=PublicityPunishment')
        soup = BeautifulSoup(response.text, "lxml")

        node = soup.find('div', class_='tabcnt')

        # 查找总页数：
        tb_text = node.text.strip()
        total_pages_ = tb_text[tb_text.find(u'为您找到相关结果'):len(tb_text)].replace(u'为您找到相关结果', '').replace(u'个', '')
        total_pages = int(total_pages_)/10

        for i in range(1,total_pages):
            url = 'http://www.hbcredit.gov.cn/credithb/gkgs/list.html?type=PublicityPunishment'
            param = {'bt': '', 'bmmc': '', 'sxmc': '', 'pageIndex': str(i), 'type': 'PublicityPunishment'}

            yield scrapy.FormRequest(url=url,formdata=param)





    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content,"lxml")
        node = soup.find('div', class_='right_xkgs')
        links = node.find_all('a')
        for link in links:
            url = link.get('href').strip()
            detail_url = 'http://www.hbcredit.gov.cn' + url
            yield scrapy.Request(url=detail_url,callback=self.parse_detail)


    def parse_detail(self,response):
        item = crawler116()
        content = response.body
        soup = BeautifulSoup(content,"lxml")

        # 按照固定格式提取页面数据
        div = soup.find('div', {'class': 'display_con'})

        tdnodes = div.find_all('td')

        data_source = '4'
        entity_name = tdnodes[1].text.strip()
        entity_type = '2'
        case_no = tdnodes[19].text.strip()
        punish_type1 = tdnodes[13].text.strip()
        punish_type2 = tdnodes[15].text.strip()
        punish_reason = tdnodes[25].text.strip()
        law_item = tdnodes[27].text.strip()
        credit_no = tdnodes[3].text.strip()
        org_code = tdnodes[5].text.strip()
        reg_no = tdnodes[7].text.strip()
        tax_no = tdnodes[9].text.strip()
        identity_card = tdnodes[21].text.strip()
        legal_man = tdnodes[11].text.strip()
        punish_result = tdnodes[29].text.strip()
        punish_date = tdnodes[17].text.strip()
        punish_agent = tdnodes[31].text.strip()
        current_status = tdnodes[33].text.strip()
        area_code = tdnodes[39].text.strip()
        offical_updtime = tdnodes[37].text.strip()
        note = tdnodes[41].text.strip()
        create_date = time.strftime('%Y-%m-%d', time.localtime())

        item['data_source'] = data_source
        item['entity_name'] = entity_name
        item['entity_type'] = entity_type
        item['case_no'] = case_no
        item['punish_type1'] = punish_type1
        item['punish_type2'] = punish_type2
        item['punish_reason'] = punish_reason
        item['law_item'] = law_item
        item['credit_no'] = credit_no
        item['org_code'] = org_code
        item['reg_no'] = reg_no
        item['tax_no'] = tax_no
        item['identity_card'] = identity_card
        item['legal_man'] = legal_man
        item['punish_result'] = punish_result
        item['punish_date'] = punish_date
        item['punish_agent'] = punish_agent
        item['current_status'] = current_status
        item['area_code'] = area_code
        item['offical_updtime'] = offical_updtime
        item['note'] = note
        item['create_date'] = create_date
        item['source_url'] = response.url
        item['source_page'] = content
        item['spider_name'] = self.name

        yield item







