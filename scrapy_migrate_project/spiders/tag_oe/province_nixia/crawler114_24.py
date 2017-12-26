# -*- coding: utf-8 -*-
# 国家企业信用信息系统(宁夏) 企业经营异常名录-列入
import scrapy
import time
from scrapy_migrate_project.items import crawler114


class Nx024InSpider(scrapy.Spider):
    name = 'crawler114_24'
    allowed_domains = ['nx.gsxt.gov.cn']
    start_urls = ['http://nx.gsxt.gov.cn/noticeAction_noticeList.action?noticeType=11&currPage=1']

    # 列表页
    def parse(self, response):
        news_li = response.xpath('//ul[@class="news_li"]/li')
        for li in news_li:
            item = crawler114()
            title = li.xpath('./p//a/text()').extract_first()
            ent_name = title.replace(u'关于', '').replace(u'移出经营异常名录公告', '')

            item['ent_name'] = ent_name
            href = li.xpath('./p//a/@href').extract_first()
            detail_url = 'http://nx.gsxt.gov.cn' + href
            item['pun_org'] = li.xpath('./p//span/text()').extract_first()
            pun_date = li.xpath('./em/text()').extract_first()
            item['pun_date'] = pun_date

            hashcode = hash(ent_name + pun_date)
            item['data_id'] = 'nx' + '-' + str(hashcode)
            item['data_source'] = self.name
            yield scrapy.Request(detail_url,
                                 callback=self.parse_detail,
                                 meta={'item': item})

        # 翻页
        url = response.url
        cur_page = url.split("currPage=")[-1]
        total_pages = response.xpath('.//input[@id="countPage"]/@value').extract_first()
        if int(cur_page) < int(total_pages):
            cur_page = int(cur_page) + 1
            next_href = 'http://nx.gsxt.gov.cn/noticeAction_noticeList.action?noticeType=11&currPage=' + str(cur_page)
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
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        item['case_no'] = response.xpath('//div[@class="tc"]/span/text()').extract_first()
        item['pun_reason'] = response.xpath('//div[@class="txt_con"]/p[1]/text()').extract_first()
        item['reg_no'] = ''
        item['del_flag'] = '0'
        item['op_flag'] = 'a'
        item['report_year'] = ''
        item['notice_id'] = ''
        yield item

