# -*- coding: utf-8 -*-
# 国家企业信用信息系统(天津) 企业经营异常名录-列入
import re
import time
import scrapy
from scrapy_migrate_project.items import crawler114


class Tj022InSpider(scrapy.Spider):
    name = 'crawler114_22'
    allowed_domains = ['tjcredit.gov.cn']
    start_urls = ['http://www.tjcredit.gov.cn/gsxt/excdir/search']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url,
                                 formdata ={'pageIndex': '1',
                                            'pageSize': '10',
                                            'entname': ''},
                                 callback= self.parse
            )

    def parse(self, response):
        li_list = response.xpath('//tbody/tr')
        for li in li_list:
            item = crawler114()
            url = response.url
            item['source_url'] = url
            item['spider_name'] = self.name
            data = response.text
            item['source_page'] = data
            ent_name = li.xpath('./td[1]/a/text()').extract_first().replace(' ', '')
            item['ent_name'] = ent_name
            item['pun_org'] = li.xpath('./td[2]/text()').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')
            item['pun_reason'] = li.xpath('./td[3]/text()').extract_first().replace('\t', '').replace('\r', '').replace('\n', '').replace(u'\xa0', u' ')
            pun_date = li.xpath('./td[5]/text()').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')
            item['pun_date'] = pun_date
            hashcode = hash(ent_name + pun_date)
            item['data_source'] = self.name
            item['del_flag'] = '0'
            item['op_flag'] = 'a'
            item['data_id'] = 'tj' + '-' + str(hashcode)
            item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
            item['case_no'] = ''
            item['reg_no'] = ''
            item['report_year'] = ''
            item['notice_id'] = ''
            yield item
        # 翻页
        url = response.url
        total_pages = re.findall('var maxPage = (.*?);', response.text)[0]
        cur_page = re.findall('var pageIndex = (.*?);', response.text)[0]
        if int(cur_page) < int(total_pages):
            next_page = int(cur_page) + 1
            yield scrapy.FormRequest(url,
                                     formdata={'pageIndex': str(next_page),
                                               'pageSize': '10',
                                               'entname': ''},
                                     callback=self.parse)