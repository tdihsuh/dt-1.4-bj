# -*- coding: utf-8 -*-
# 国家企业信用信息系统(青海) 企业经营异常名录-移出
import re
import scrapy
import time

from scrapy_migrate_project.items import crawler114_out


class Qh021OutSpider(scrapy.Spider):
    name = 'crawler114_o_21'
    allowed_domains = ['qh.gsxt.gov.cn']
    start_urls = ['http://qh.gsxt.gov.cn/ycmlNoticeInfo.jspx?mark=02&pageNo=1&order=0&title=&area=']

    def parse(self, response):
        li_list = response.xpath('//table/tr')[:-1]
        for li in li_list:
            item = crawler114_out()

            title = li.xpath('./td[2]/a/text()').extract_first()
            ent_name = title.replace(u'关于', '').replace(u'企业移出经营异常名录公告', '')
            ent_name = ent_name.replace(' ', '').replace('\r\n', '').replace(u'\xa0', u' ')
            item['ent_name'] = ent_name
            item['release_org'] = li.xpath('./td[@id="A5"]/text()').extract_first()
            item['release_org'] = item['release_org'].replace(' ', '').replace('\r\n', '')
            release_date = li.xpath('./td[@class="td4"]/span/text()').extract_first()
            item['release_date'] = release_date
            if release_date:
                hashcode = hash(ent_name + release_date)
            else:
                hashcode = hash(ent_name)
            item['data_source'] = self.name
            item['data_id'] = 'qh' + '-' + str(hashcode)
            detail_url = li.xpath('.//a[@id="A3"]/@href').extract_first()
            detail_url = 'http://qh.gsxt.gov.cn/' + detail_url
            yield scrapy.Request(detail_url,
                                 callback=self.parse_detail,
                                 meta={'item': item})

        # 翻页
        # 总页数
        url = response.url
        ret = response.xpath('.//div[@class="newfy"]/ul/li[2]/text()').extract_first()
        total_pages = re.findall('.*?(\d+).*?', ret)[0]
        # 当前页
        cur_page = url.split('pageNo=')[-1].split('&')[0]
        if int(cur_page) < int(total_pages):
            next_page = int(cur_page) + 1
            next_url = 'http://qh.gsxt.gov.cn/ycmlNoticeInfo.jspx?mark=02&pageNo=' + str(
                next_page) + '&order=0&title=&area='
            yield scrapy.Request(next_url,
                                 callback=self.parse)

    # 详情页
    def parse_detail(self, response):
        item = response.meta['item']
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        data = response.text
        item['source_page'] = data
        item['case_no'] = response.xpath('//div[@class="Section1"]/p[3]/span/span[1]/text()').extract_first()
        item['release_reason'] = response.xpath('//div[@class="Section1"]/p[5]/text()').extract_first().replace(' ', '')
        item['release_reason'] = item['release_reason'].replace(' ', '').replace('\r\n', '').replace(u'\xa0', u' ')
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        item['reg_no'] = ''
        yield item
