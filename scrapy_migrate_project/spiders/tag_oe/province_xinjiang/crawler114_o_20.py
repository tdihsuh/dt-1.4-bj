# -*- coding: utf-8 -*-
# 国家企业信用信息系统(新疆) 企业经营异常名录-移出
import scrapy
import re
import time
from scrapy_migrate_project.items import crawler114_out


class Xj020OutSpider(scrapy.Spider):
    name = 'crawler114_o_20'
    allowed_domains = ['xj.gsxt.gov.cn']
    start_urls = ['http://xj.gsxt.gov.cn/xxgg/xxggAction!queryGgxx.dhtml?name=&code=&notitype=12&noticeTitle=%E8%AF%B7%E8%BE%93%E5%85%A5%E9%9C%80%E8%A6%81%E6%9F%A5%E8%AF%A2%E4%BF%A1%E6%81%AF&pageNos=1']

    def parse(self, response):
        li_list = response.xpath('//table[@class="noticelist-t"]/tr')
        for li in li_list:
            item = crawler114_out()
            title = li.xpath('./td[1]/a/text()').extract_first()

            href = li.xpath('./td[1]/a/@href').extract_first()
            href = 'http://xj.gsxt.gov.cn' + href
            item['release_org'] = li.xpath('./td[2]/text()').extract_first()
            release_date = li.xpath('./td[3]/text()').extract_first()

            item['release_date'] = release_date
            item['ent_name'] = title.replace(u'关于', '').replace(u'移出经营异常名录公告', '')
            hashcode = hash(title + release_date)

            item['data_id'] = 'xj' + '-' + str(hashcode)
            yield scrapy.Request(href,
                                 callback=self.parse_detail,
                                 meta={'item': item})

        # 翻页
        url = response.url
        cur_page = url.split('pageNos=')[-1]
        total_pages = response.xpath('//div[@class="pages"]/span[2]/text()').extract_first()
        total_pages = total_pages.replace(u'\xa0', u' ')
        total_pages = re.findall('.*?(\d+).*?', total_pages)[0]

        if int(cur_page) < int(total_pages):
            next_page = int(cur_page) + 1
            next_href = 'http://xj.gsxt.gov.cn/xxgg/xxggAction!queryGgxx.dhtml?name=&code=&notitype=12&noticeTitle=%E8%AF%B7%E8%BE%93%E5%85%A5%E9%9C%80%E8%A6%81%E6%9F%A5%E8%AF%A2%E4%BF%A1%E6%81%AF&pageNos=' + str(
                next_page)
            yield scrapy.Request(next_href,
                                 callback=self.parse)


     # 详情页
    def parse_detail(self, response):
        item = response.meta['item']
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        data = response.text
        item['source_page'] = data
        item['release_reason'] = response.xpath('//div[@class="box"]/div/p[2]/text()').extract_first().replace(u'\xa0', u' ')
        item['data_source'] = self.name
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        yield item
