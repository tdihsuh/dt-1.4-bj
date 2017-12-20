# -*- coding: utf-8 -*-
import json

import requests
import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler114_out


class Crawler1146OutSpider(scrapy.Spider):
    name = 'crawler114_6_out'
    allowed_domains = ['yn.gsxt.gov.cn']

    headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.8", "Connection": "keep-alive",
               "Cookie": "JSESSIONID_NOTICE=c4lOABfoSGX2IQVCTZYg1aZUd6IHvcoAraZULENNJh4HfIK3VAxc!-902616556; UM_distinctid=15d2f3332fc3c0-09042104ddbf9-8383667-1fa400-15d2f3332fd24d; Hm_lvt_cdb4bc83287f8c1282df45ed61c4eac9=1499735471; notice=76439977; CNZZDATA1000298231=448861924-1500251596-http%253A%252F%252Fsd.gsxt.gov.cn%252F%7C1500251596",
               "Host": "yn.gsxt.gov.cn",
               "Referer": "http://yn.gsxt.gov.cn/notice/search/ent_announce",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
               "X-Requested-With": "XMLHttpRequest"}

    def start_requests(self):
        url_page = 'http://yn.gsxt.gov.cn/notice/search/GET/announce?type=0102&mode=all&pageNo=1&areaId=&keyword='
        r = requests.get(url_page, headers=self.headers)
        json_content = r.json()
        totalpages = json_content["result"]["pageCount"]

        for i in range(1, totalpages + 1):
            url = 'http://yn.gsxt.gov.cn/notice/search/GET/announce?type=0102&mode=all&pageNo=' + str(
                i) + '&areaId=&keyword='
            yield scrapy.Request(url=url, headers=self.headers)

    def parse(self, response):
        content = response.body
        json_content = json.loads(content)
        data_content_list = json_content["result"]["data"]

        for each in data_content_list:
            detail_link_ = each["link"]
            detail_link = 'http://yn.gsxt.gov.cn/notice/search/announce_detail?uuid=' + detail_link_ + '&category=01&categorySub=01'
            ent_name = each["etpName"].replace(u'移出经营异常名录', '').replace(u'公告', '')
            release_date = each["date"]
            release_org = each["orgName"]
            title = each["etpName"]

            yield scrapy.Request(url=detail_link,
                                 meta={"ent_name": ent_name, "release_date": release_date, "release_org": release_org},
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        item = crawler114_out()
        content = response.body
        soup = BeautifulSoup(content, "lxml")

        tag_p = soup.find_all('p')
        if len(tag_p) >= 2:
            case_no = tag_p[0].get_text(strip=True)
            release_reason = tag_p[1].get_text(strip=True)
        else:
            case_no = None
            release_reason = None

        data_source = 'crawler114_6_out'
        create_date = time.strftime('%Y-%m-%d', time.localtime())

        item['case_no'] = case_no
        item['release_org'] = response.meta['release_org']
        item['release_date'] = response.meta['release_date']
        item['entity_name'] = response.meta['ent_name']
        item['release_reason'] = release_reason
        item['data_source'] = data_source
        item['create_date'] = create_date
        item['source_url'] = response.url
        item['source_page'] = content
        item['data_id'] = 'yunnan'
        item['spider_name'] = self.name

        yield item
