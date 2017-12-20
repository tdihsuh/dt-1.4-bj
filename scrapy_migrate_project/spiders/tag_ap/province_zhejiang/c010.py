# -*- coding: utf-8 -*-
"""杭州行政处罚"""
import scrapy
import json
import time
from scrapy_migrate_project.items import C010Item

class C010Spider(scrapy.Spider):
    name = 'c010'
    allowed_domains = ['www.hzcredit.gov.cn']
    url = 'http://www.hzcredit.gov.cn/lzonghe641/queryLzonghe641'
    formdata={'code': '1',
              'page': '1',
                'count': '10',
               'peopleValue': '',
               'nameValue': '',
               'dateStart': '',
             'dateEnd': ''}
    def start_requests(self):
        yield scrapy.FormRequest(self.url,
                                 formdata=self.formdata,
                                 dont_filter=True,
                                 )
    def parse(self, response):
        res=json.loads(response.text)
        total=res['totalCount']
        pages=total/10 if total%10==0 else int(total/10)+1
        for page in range(1,1+pages):
            self.formdata['page']=str(page)
            yield scrapy.FormRequest(self.url,
                                 formdata=self.formdata,
                                 dont_filter=True,
                                     callback=self.parseJson
                                     )
    def parseJson(self,response):
        detaildic=json.loads(response.text)['list641']

        for jj in range(len(detaildic)):
            item = C010Item()
            item['notice_id'] = detaildic[jj]['sysid']  # 系统编码
            item['filenum'] = detaildic[jj]['f01']
            item['punishname'] = detaildic[jj]['f02']
            item['punishtype'] = detaildic[jj]['f03']
            item['punishreason'] = detaildic[jj]['f05']
            item['punishaccordance'] = detaildic[jj]['f06']
            item['personname'] = detaildic[jj]['f07']
            item['idcard'] = detaildic[jj]['f12']
            item['punishresult'] = detaildic[jj]['f14']
            item['punishdepartment'] = detaildic[jj]['f16']
            item['spider_name']=self.name
            # item['source_page']=response.text
            yield item