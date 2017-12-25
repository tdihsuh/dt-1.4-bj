# -*- coding: utf-8 -*-
#  国家企业信用信息系统(吉林) 企业经营异常名录移出
import scrapy
import time,json
from scrapy_migrate_project.items import crawler114_out


class Jl023OutSpider(scrapy.Spider):
    name = 'crawler114_o_23'
    allowed_domains = ['jl.gsxt.gov.cn']
    start_urls = ['http://jl.gsxt.gov.cn/api/Common/AfficheInfos?type=1&subType=12&keyWord=&page=1&judauth=']

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
            url = 'http://jl.gsxt.gov.cn/api/Common/AfficheInfos?type=1&subType=12&keyWord=&page=' + str(
                cur_page) + '&judauth='
            yield scrapy.Request(url,
                                 callback=self.parse)

    # 详情页
    def parse_detail(self, response):
        item = crawler114_out()
        data = json.loads(response.body.decode('utf-8'))
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        item['case_no'] = data['NOTNO']
        ent_name = data['ENTNAME']
        item['ent_name'] = ent_name
        release_org = data['DECORGNAME']
        item['release_org'] = release_org
        release_date = data['ABNTIMEString']
        item['release_date'] = release_date
        reg_no = data['REGNO']
        item['reg_no'] = reg_no
        pun_reason1 = data['FACTANDRULE']
        pun_reason2 = data['BASISINFO']
        release_reason = u'经查，你单位因' + pun_reason1 + u'，违反了' + pun_reason2 + u'的规定，现决定将其列入经营异常名录。'
        item['release_reason'] = release_reason
        item['data_source'] = self.name
        hashcode = hash(ent_name + release_date)
        item['data_id'] = 'jl' + '-' + str(hashcode)
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        data = response.text
        item['source_page'] = data
        yield item