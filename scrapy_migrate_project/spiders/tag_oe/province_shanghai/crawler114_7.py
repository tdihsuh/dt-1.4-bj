# -*- coding: utf-8 -*-
import json

import requests
import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler114


class Crawler1147Spider(scrapy.Spider):
    name = 'crawler114_7'
    allowed_domains = ['sh.gsxt.gov.cn']

    headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Cookie": "UM_distinctid=15fe78ed49f188-0757ac673c0b39-7b113d-1fa400-15fe78ed4a07bb; Hm_lvt_cdb4bc83287f8c1282df45ed61c4eac9=1511493814,1511750084,1511921401,1511924894; pgv_pvi=1583393792; JSESSIONIDNOTICE=0000r_t7QTYehD2qDHgZZIBTfYD:1b2331sgt",
               "Host": "sh.gsxt.gov.cn", "Referer": "http://sh.gsxt.gov.cn/notice/search/ent_announce",
               "X-Requested-With": "XMLHttpRequest",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    def start_requests(self):
        url_page = 'http://sh.gsxt.gov.cn/notice/search/GET/announce?type=0101&mode=all&pageNo=1&areaId=&keyword='
        r = requests.get(url_page, headers=self.headers)
        json_content = r.json()
        totalpages = json_content["result"]["pageCount"]
        print(totalpages)
        for i in range(1, totalpages+1):
            url = 'http://sh.gsxt.gov.cn/notice/search/GET/announce?type=0101&mode=all&pageNo=' + str(
                i) + '&areaId=&keyword='
            yield scrapy.Request(url=url, headers=self.headers)

    def parse(self, response):
        content = response.body
        json_content = json.loads(content)
        data_content_list = json_content["result"]["data"]
        data_length = len(json_content["result"]["data"])
        for each in data_content_list:
            detail_link_ = each["link"]
            detail_link = 'http://sh.gsxt.gov.cn/notice/search/announce_detail?uuid=' + detail_link_ + '&category=01&categorySub=01'
            ent_name = each["etpName"].replace(u'列入经营异常名录', '')
            pun_date = each["date"]
            pun_org = each["orgName"]
            title = each["etpName"]

            yield scrapy.Request(url=detail_link, meta={"ent_name": ent_name, "pun_date": pun_date, "pun_org": pun_org},
                                 callback=self.parse_detail)

    def parse_detail(self,response):
        item = crawler114()
        content = response.body
        soup = BeautifulSoup(content,"lxml")
        tag_p = soup.find_all('p')

        case_no = tag_p[0].get_text(strip=True).replace(u'公告号：', '')
        pun_reason = tag_p[1].get_text(strip=True)

        data_source = 'crawler114_7'
        del_flag = '0'
        op_flag = 'a'
        create_date = time.strftime('%Y-%m-%d', time.localtime())

        item['case_no'] = case_no
        item['pun_org'] = response.meta['pun_org']
        item['pun_date'] = response.meta['pun_date']
        item['ent_name'] = response.meta['ent_name']
        item['pun_reason'] = pun_reason
        item['data_source'] = data_source
        item['data_id'] = 'shanghai'
        item['del_flag'] = del_flag
        item['op_flag'] = op_flag
        item['create_date'] = create_date
        item['source_url'] = response.url
        item['source_page'] = content
        item['spider_name'] = self.name

        yield item
