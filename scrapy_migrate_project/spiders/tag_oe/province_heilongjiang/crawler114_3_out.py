# -*- coding: utf-8 -*-
import urllib2

import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler114_out


class Crawler1143OutSpider(scrapy.Spider):
    name = 'crawler114_3_out'
    allowed_domains = ['gsxt.hljaic.gov.cn']

    def start_requests(self):
        baseurl = 'http://gsxt.hljaic.gov.cn/ycmlNoticeInfo.jspx?mark=02&title=&area=&pageNo=' + str(
            0) + '&t=Mon%20Jul%2010%202017%2017:09:36%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
        response = urllib2.urlopen(baseurl)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        tag_div = soup.find_all('div', attrs={"class": "newfy", "id": "lrycml"})
        page_content = tag_div[0].find_all('li')
        page_str_temp = page_content[1].get_text(strip=True).encode('utf-8')
        pages_str = filter(str.isalnum, page_str_temp)
        total_pages = int(pages_str)

        for i in range(1, total_pages):
            url = 'http://gsxt.hljaic.gov.cn/ycmlNoticeInfo.jspx?mark=02&title=&area=&pageNo=' + str(i
                                                                                                     ) + '&t=Mon%20Jul%2010%202017%2017:09:36%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
            yield scrapy.Request(url=url)

    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content, "lxml")

        tag_tr = soup.find_all('tr')
        for i in range(0, len(tag_tr) - 1):
            list_temp = []
            tag_a = tag_tr[i].find_all(id="A3")
            tag_td = tag_tr[i].find_all(id="A5")
            tag_td2 = tag_tr[i].find_all(class_="td4")
            pun_date = tag_td2[0].get_text(strip=True)
            pun_org = tag_td[0].get_text(strip=True)
            detail_url_ = tag_a[0]["href"]
            detail_url = 'http://gsxt.hljaic.gov.cn/' + detail_url_
            title = tag_a[0]["title"]
            id_temp = detail_url.split('=')
            id = id_temp[1]

            yield scrapy.Request(url=detail_url, meta={"pun_date": pun_date, "pun_org": pun_org, "title": title},callback=self.parse_detail)


    def parse_detail(self,response):
        item = crawler114_out()
        content = response.body
        soup = BeautifulSoup(content, "lxml")

        tag_p = soup.find_all('p', attrs={"class": False})
        tag_span = soup.find_all('span', attrs={"lang": "EN-US"})

        case_no = tag_span[3].get_text(strip=True)
        ent_name = tag_p[8].get_text(strip=True).encode('utf-8').replace('：', '')
        reason = tag_p[9].get_text(strip=True).encode('utf-8').replace(' ', '')
        release_org = response.meta['pun_org']
        release_date = response.meta['pun_date']
        data_id = 'hlj'
        data_source = 'crawler114_3_out'

        create_date = time.strftime('%Y-%m-%d', time.localtime())

        item['case_no'] = case_no
        item['release_org'] = release_org
        item['release_date'] = release_date
        item['ent_name'] = ent_name
        item['release_reason'] = reason
        item['data_id'] = data_id
        item['data_source'] = data_source
        item['create_date'] = create_date
        item['source_url'] = response.url
        item['source_page'] = content

        yield item

