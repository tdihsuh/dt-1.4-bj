# -*- coding: utf-8 -*-
#  国家企业信用信息系统(吉林) 企业经营异常名录列入
import scrapy
import time,json
from scrapy_migrate_project.items import crawler114


class Jl023InSpider(scrapy.Spider):
    name = 'crawler114_23'
    allowed_domains = ['jl.gsxt.gov.cn']
    start_urls = ['http://jl.gsxt.gov.cn/api/Common/AfficheInfos?type=1&subType=11&keyWord=&page=1&judauth=']

    # 列表页
    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))
        li_list = data['data']
        for li in li_list:
            ggid = li['gsggId']
            href = 'http://jl.gsxt.gov.cn/api/Common/AffAbnoper/' + ggid
            yield scrapy.Request(href,
                                 callback=self.parse_detail,
                                 )

        # 翻页
        url = response.url
        cur_page = url.split("page=")[-1].split('&')[0]
        print cur_page
        pages = data['recordsFiltered']
        if int(cur_page) < int(pages):
            cur_page = int(cur_page) + 1
            url = 'http://jl.gsxt.gov.cn/api/Common/AfficheInfos?type=1&subType=11&keyWord=&page=' + str(
                cur_page) + '&judauth='
            yield scrapy.Request(url,
                                 callback=self.parse)

    # 详情页
    def parse_detail(self, response):
        item = crawler114()
        data = json.loads(response.body.decode('utf-8'))
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        item['source_page'] = data
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        item['case_no'] = data['NOTNO']
        ent_name = data['ENTNAME']
        item['ent_name'] = ent_name
        pun_org = data['DECORGNAME']
        item['pun_org'] = pun_org
        pun_date = data['ABNTIMEString']
        item['pun_date'] = pun_date
        reg_no = data['REGNO']
        item['reg_no'] = reg_no
        pun_reason1 = data['FACTANDRULE']
        pun_reason2 = data['BASISINFO']
        pun_reason = u'经查，你单位因' + pun_reason1 + u'，违反了' + pun_reason2 + u'的规定，现决定将其列入经营异常名录。'
        item['pun_reason'] = pun_reason
        item['del_flag'] = '0'
        item['op_flag'] = 'a'
        item['data_source'] = self.name
        hashcode = hash(ent_name + pun_date)
        item['data_id'] = 'jl' + '-' + str(hashcode)
        yield item
