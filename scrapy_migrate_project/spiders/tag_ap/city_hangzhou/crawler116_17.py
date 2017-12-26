# -*- coding: utf-8 -*-
# 信用杭州
import json
import re
from scrapy_migrate_project.items import crawler116
import scrapy


class Hz017Spider(scrapy.Spider):
    name = 'crawler116_17'
    allowed_domains = ['hzcredit.gov.cn']
    url = 'http://220.191.208.234/fbpt/appAction.do'
    formdata = {
        'dispatch': 'querySgs',
        'deptId': '0',
        'choose': '2',
        'page': '1',
        'xdrName': '',
        'projectName': '',
        'datestart': '',
        'dateEnd': ''
    }
    patt = re.compile(r'\d+\.\d+\.\d+\.\d+')

    def start_requests(self):
        yield scrapy.FormRequest(self.url,
                                 formdata=self.formdata
                                 )

    def parse(self, response):
        if not self.patt.search(response.text):
            r = json.loads(response.text.split('</script>')[-1])
            pagesize = 10
            total = r.get('count')
            totalpages = total // pagesize if total % pagesize == 0 else total // pagesize + 1
            print(totalpages, type(totalpages))

            for page in range(1, int(totalpages)):
                self.formdata['page'] = str(page)
                yield scrapy.FormRequest(self.url,
                                         formdata=self.formdata,
                                         dont_filter=True,
                                         callback=self.parseJson)

    def parseJson(self, response):
        if not self.patt.search(response.text):
            r = json.loads(response.text.split('</script>')[-1])
            lists = r['list']
            for data in lists:
                item = crawler116()
                item['entity_name'] = data['xdrName']
                item['org_code'] = data['enterpriseId']
                item['case_no'] = data['jds']
                item['punish_agent'] = data['deptName']
                item['law_item'] = data['cfyj']
                item['punish_result'] = data['cfjg']
                item['punish_reason'] = data['content']
                item['notice_id'] = data['sysId']
                item['punish_date'] = data['dateStart']
                url = response.url
                item['source_url'] = url
                item['spider_name'] = self.name
                ret = response.text
                item['source_page'] = ret
                item['punish_type1'] = ''
                item['credit_no'] = ''
                item['reg_no'] = ''
                item['tax_no'] = ''
                item['identity_card'] = ''
                item['legal_man'] = ''
                item['current_status'] = ''
                item['area_code'] = ''
                item['offical_updtime'] = ''
                item['note'] = ''
                item['create_date'] = ''
                item['update_date'] = ''
                item['punish_type2'] = ''
                item['entity_type'] = ''
                item['data_source'] = ''
                yield item

