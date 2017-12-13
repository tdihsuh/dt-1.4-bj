# -*- coding: utf-8 -*-
import requests
import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler114_out


class Crawler1145OutSpider(scrapy.Spider):
    name = 'crawler114_5_out'
    allowed_domains = ['ha.gsxt.gov.cn']

    header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.8", "Cache-Control": "max-age=0",
               "Connection": "keep-alive",
               "Cookie": "UM_distinctid=15d2f3332fc3c0-09042104ddbf9-8383667-1fa400-15d2f3332fd24d; Hm_lvt_cdb4bc83287f8c1282df45ed61c4eac9=1499735471; JSESSIONID=0000GZE7-rE2_pz_9t0TpqRUpWe:-1; test=20111114; AD_VALUE=d248141d",
               "Host": "ha.gsxt.gov.cn", "Referer": "http://ha.gsxt.gov.cn/infoAnnoucement.jspx?ad_check=1",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

    def start_requests(self):
        url_page = 'http://ha.gsxt.gov.cn/ycmlNoticeInfo.jspx?mark=02&title=&area=&pageNo=1&t=Thu%20Jul%2013%202017%2009:08:05%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
        r = requests.get(url_page, headers=self.header)
        soup = BeautifulSoup(r.text, "lxml")
        tag_div = soup.find_all(id='lrycml')
        page_content = tag_div[0].find_all('ul')[0].find_all('li')[1].get_text(strip=True).encode('utf-8')
        total_pages = int(filter(str.isalnum, page_content))

        for i in range(1,total_pages):
            url = 'http://ha.gsxt.gov.cn/ycmlNoticeInfo.jspx?mark=02&title=&area=&pageNo=' + str(
                i) + '&t=Thu%20Jul%2013%202017%2009:08:05%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
            yield scrapy.Request(url=url,headers=self.header)

    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content,"lxml")
        tag_a = soup.find_all('table')[0].find_all('tr')
        for each in tag_a:
            tags_td = each.find_all('td')
            title = tags_td[1].get_text().encode('utf-8')
            release_org = tags_td[2].get_text().encode('utf-8')
            release_date = tags_td[3].get_text().encode('utf-8')
            ent_name = title.replace('关于', '').replace('企业移出经营异常名录公告', '')
            try:
                detail_url = 'http://ha.gsxt.gov.cn' + tags_td[1].find_all('a')[0]['href']
            except:
                continue

            yield scrapy.Request(url=detail_url, meta={"release_org": release_org, "release_date": release_date, "ent_name": ent_name},
                                 callback=self.parse_detail)

    def parse_detail(self,response):
        content = response.body
        soup = BeautifulSoup(content,"lxml")
        item = crawler114_out()
        release_reason = soup.find_all(class_='Section1')[0].find_all('p')[1].get_text()
        create_date = time.strftime('%Y-%m-%d', time.localtime())
        data_id = 'henan'
        data_source = 'crawler114_5_out'
        item['release_reason'] = release_reason
        item['ent_name'] = response.meta['ent_name']
        item['release_org'] = response.meta['release_org']
        item['release_date'] = response.meta['release_date']
        item['source_url'] = response.url
        item['source_page'] = content
        item['create_date'] = create_date
        item['data_id'] = data_id
        item['data_source'] = data_source

        yield item