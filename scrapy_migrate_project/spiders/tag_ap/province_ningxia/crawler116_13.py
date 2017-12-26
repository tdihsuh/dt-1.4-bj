# -*- coding: utf-8 -*-
# 信用宁夏
import json
from urllib import unquote
import scrapy
from scrapy_migrate_project.items import crawler116


class Nx013Spider(scrapy.Spider):
    name = 'crawler116_13'
    allowed_domains = ['nxcredit.gov.cn']
    start_urls = ['http://www.nxcredit.gov.cn/lXzcfList.jspx']

    # 列表页
    def parse(self, response):
        li_list = response.xpath('//ul[@id="search-result-list"]')
        for li in li_list:
            href = li.xpath('./li/a/@href').extract_first()
            href = href.split('jspx?')[-1]
            href = 'http://www.nxcredit.gov.cn/xyxx/xzcf.jspx?' + href + '&dataType=1&tableTab=&page=1&pageSize=10&pageNo=1'
            yield scrapy.Request(href,
                                 callback=self.parse_detail)

        # 翻页
        area_list = ['640100', '640200', '640300', '640400', '640500']
        for area in area_list:
            formdata = {
                'searchContent': '',
                'areacode': area,
                'pageNo_sgs': '1'
            }
            url = 'http://www.nxcredit.gov.cn/lXzcfList.jspx?type=2'
            yield scrapy.FormRequest(url,
                                     formdata=formdata,
                                     callback=self.parse
                                     )

    # 详情页
    def parse_detail(self, response):
        pass
        r = json.loads(response.text)
        for data in r['result']['data']['list']:
            item = crawler116()
            item['law_item'] = data.get('cfYj')
            item['punish_result'] = data.get('cfJg')
            item['punish_reason'] = data.get('cfSy')
            item['case_no'] = data.get('cfWsh')
            item['punish_agent'] = data.get('cfXzjg')
            item['punish_type1'] = data.get('cfJg')
            item['punish_date'] = data.get('publishDate')
            item['legal_man'] = unquote(response.url.split('legalPerson=')[-1].split('&')[0])
            item['credit_no'] = unquote(response.url.split('tyshxydm=')[-1].split('&')[0])
            url = response.url
            item['source_url'] = url
            item['spider_name'] = self.name
            data = response.text
            item['source_page'] = data
            item['entity_name'] = ''
            item['org_code'] = ''
            item['reg_no'] = ''
            item['tax_no'] = ''
            item['identity_card'] = ''
            item['current_status'] = ''
            item['area_code'] = ''
            item['offical_updtime'] = ''
            item['note'] = ''
            item['create_date'] = ''
            item['update_date'] = ''
            item['punish_type2'] = ''
            item['entity_type'] = ''
            item['data_source'] = ''
            item['notice_id'] = ''
            yield item
