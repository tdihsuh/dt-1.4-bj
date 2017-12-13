# -*- coding: utf-8 -*-
import urllib2

import scrapy
import json

import time
from bs4 import BeautifulSoup
import lxml

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy_migrate_project.items import TourismItem


class TourismSpiderSpider(scrapy.Spider):
    name = 'tourism_spider'
    allowed_domains = ['qualitytourism.cnta.gov.cn']

    def start_requests(self):
        baseurl = 'http://qualitytourism.cnta.gov.cn/tools/submit_ajax.ashx?action=searchpbadinfo&type=%u5168%u90E8%u4F01%u4E1A&page='
        pagee = 1
        url = baseurl + str(pagee)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        ajax = json.loads(html)
        ajaxp = ajax['p']
        soup = BeautifulSoup(ajaxp, "lxml")
        pagetag = soup.find_all('span')
        page = pagetag[0].get_text(strip=True).encode('utf-8')
        totalitems = filter(str.isalnum, page)
        totalitems = int(totalitems)

        if totalitems % 10 == 0:
            totalpages = totalitems / 10
        else:
            totalpages = totalitems // 10 + 1

        for i in range(totalpages):
            baseurl = 'http://qualitytourism.cnta.gov.cn/tools/submit_ajax.ashx?action=searchpbadinfo&type=%u5168%u90E8%u4F01%u4E1A&page='
            pagee = i + 1
            url = baseurl + str(pagee)

            yield scrapy.Request(url=url)

    def parse(self, response):
        content = response.body
        content_json = json.loads(content)
        d_set = content_json['d1']
        for each in d_set:
            id = each['ID']

            url_detail = 'http://qualitytourism.cnta.gov.cn/badinfo/show-' + str(id) + '.html'
            yield scrapy.Request(url=url_detail, callback=self.parse_detail)

    def parse_detail(self, response):
        content = response.body
        soup2 = BeautifulSoup(content, "lxml")

        detail = soup2.find_all(class_='d_texty')
        detail2 = soup2.find_all(id='cop_name')
        detail3 = soup2.find_all(id='cop_LegalPerson')
        detail4 = soup2.find_all(id='cop_permitnumber')
        detail5 = soup2.find_all(id='cop_PenaltyContent')
        detail6 = soup2.find_all(id='cop_Reason')
        detailStarttime_year = soup2.find_all(id='cop_sy')
        detailStarttime_month = soup2.find_all(id='cop_sm')
        detailStarttime_day = soup2.find_all(id='cop_sd')

        detailStarttime = detailStarttime_year[0].get_text() + '-' + detailStarttime_month[0].get_text() + '-' + \
                          detailStarttime_day[0].get_text()

        detailEndtime_year = soup2.find_all(id='cop_ey')
        detailEndtime_month = soup2.find_all(id='cop_em')
        detailEndtime_day = soup2.find_all(id='cop_ed')

        detailEndtime = detailEndtime_year[0].get_text() + '-' + detailEndtime_month[0].get_text() + '-' + \
                        detailEndtime_day[0].get_text()
        penaltyby = '《旅游经营服务不良信息管理办法（试行）》'
        create_date = time.strftime('%Y-%m-%d', time.localtime())

        item = TourismItem()
        item['name'] = detail2[0].get_text()
        item['legal_person'] = detail3[0].get_text()
        item['permit_number'] =detail4[0].get_text()
        item['penalty_reason'] =detail6[0].get_text()
        item['penalty_content'] =detail5[0].get_text()
        item['penalty_by'] =penaltyby
        item['start_time'] =detailStarttime
        item['end_time'] =detailEndtime
        item['description'] =detail[0].get_text().replace(' ', '')
        item['create_date'] =create_date
        item['source_url'] = response.url
        item['source_page'] = content


        yield item

