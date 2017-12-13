# -*- coding: utf-8 -*-
import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler114


class Crawler1141Spider(scrapy.Spider):
    name = 'crawler114_1'
    allowed_domains = ['bj.gsxt.gov.cn']
    start_urls = ['http://bj.gsxt.gov.cn/']

    def start_requests(self):
        for i in range(1,3):
            url = 'http://bj.gsxt.gov.cn/xxgg/xxggAction!queryGgxx.dhtml?name=&code=&notitype=11&noticeTitle=%E8%AF%B7%E8%BE%93%E5%85%A5%E9%9C%80%E8%A6%81%E6%9F%A5%E8%AF%A2%E4%BF%A1%E6%81%AF&pageNos=' + str(
        i)
            yield scrapy.Request(url=url)

    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content, "lxml")
        tr_tags = soup.find_all('table', {"class": "noticelist-t"})[0].find_all('tr')

        for i in range(len(tr_tags)):
            title = tr_tags[i].find_all('a')[0].get_text(strip=True)
            detail_url_ = tr_tags[i].find_all('a')[0]["href"]
            detail_url = 'http://bj.gsxt.gov.cn' + detail_url_
            ent_name = title.replace(u'关于', '').replace(u'企业列入经营异常名录公告', '')
            pun_org = tr_tags[i].find_all('td')[1].get_text(strip=True)
            pun_date = tr_tags[i].find_all('td')[2].get_text(strip=True)

            yield scrapy.Request(url=detail_url,meta={'ent_name':ent_name,'pun_org':pun_org,'pun_date':pun_date,'title':title},callback=self.parse_detail)


    def parse_detail(self,response):
        item = crawler114()
        content = response.body
        soup = BeautifulSoup(content, "lxml")
        p_tags = soup.find_all('p')
        pun_reason = p_tags[1].get_text(strip=True).replace(' ', '')
        create_date = time.strftime('%Y-%m-%d', time.localtime())

        item['ent_name'] = response.meta['ent_name']
        item['pun_org'] = response.meta['pun_org']
        item['pun_date'] = response.meta['pun_date']
        item['ent_name'] = response.meta['ent_name']
        item['pun_reason'] = pun_reason
        item['data_id'] = 'qinghai'
        item['data_source'] = 'crawler114_1'
        item['del_flag'] = '0'
        item['op_flag'] = 'a'
        item['create_date'] = create_date
        item['source_url'] = response.url
        item['source_page'] = content

        yield item

