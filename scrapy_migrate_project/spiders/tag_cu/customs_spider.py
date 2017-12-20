# -*- coding: utf-8 -*-
import json

# from cycredit.RedisUtil import RedisUtil as redis
import requests
import scrapy

from scrapy_migrate_project.items import CustomsItem


class CustomsSpiderSpider(scrapy.Spider):
    name = 'customs_spider'
    allowed_domains = ['*']

    def start_requests(self):
        param = {'ccppListQueryRequest.manaType': 'C', 'ccppListQueryRequest.casePage.curPage': '1',
                 'ccppListQueryRequest.casePage.pageSize': '500'}

        r = requests.post('http://credit.customs.gov.cn/ccppAjax/queryLostcreditList.action', data=param)
        result = r.json()

        lista = result['responseResult']['responseData']['casePage']
        total_pages = lista['totalPages']

        for i in range(1, 5):
            param = {'ccppListQueryRequest.manaType': 'C', 'ccppListQueryRequest.casePage.curPage': str(i),
                     'ccppListQueryRequest.casePage.pageSize': '500'}

            url = 'http://credit.customs.gov.cn/ccppAjax/queryLostcreditList.action'

            yield scrapy.FormRequest(url=url, formdata={'ccppListQueryRequest.manaType': 'C',
                                                        'ccppListQueryRequest.casePage.curPage': str(i),
                                                        'ccppListQueryRequest.casePage.pageSize': '500'})

    def parse(self, response):
        content = response.body
        result = json.loads(content)
        item = CustomsItem()

        for each in result['responseResult']['responseData']['copInfoResultList']:
            copname = each['nameSaic'].replace(' ', '')
            org_code = each['saicSysNo']
            creditcode = each['socialCreditCode']

            hashcode = hash(copname+org_code+creditcode)


            item['copname'] = copname
            item['org_code'] = org_code
            item['creditcode'] = creditcode
            item['source_url'] = response.url
            item['source_page'] = content
            item['spider_name'] = self.name

            yield item
