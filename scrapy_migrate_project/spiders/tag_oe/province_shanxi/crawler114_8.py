# -*- coding: utf-8 -*-
import requests
import scrapy
import time

from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler114


class Crawler1148Spider(scrapy.Spider):
    count = 0
    name = 'crawler114_8'
    allowed_domains = ['sn.gsxt.gov.cn']
    timstamp = int(time.time())
    headers_list = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
               "Cache-Control": "max-age=0", "Connection": "keep-alive",
               "Content-Length": "206", "Content-Type": "application/x-www-form-urlencoded",
               "Cookie": "UM_distinctid=15d2f3332fc3c0-09042104ddbf9-8383667-1fa400-15d2f3332fd24d; Hm_lvt_cdb4bc83287f8c1282df45ed61c4eac9=1499735471,1500601585; JSESSIONID=VDgyZ2qDjq6c1k6KFKh07zcqkpnhDfwV3mVLfLwyjx3Y1Jv0hMhJ!-699126804; CNZZDATA1256107480=538513944-1500267535-http%253A%252F%252Fsn.gsxt.gov.cn%252F%7C1500947649",
               "Host": "sn.gsxt.gov.cn", "Origin": "http://sn.gsxt.gov.cn",
               "Referer": "http://sn.gsxt.gov.cn/xxcx.do?method=xxggList&xxlx=1&status=2&random=" + str(timstamp),
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

    headers_detail = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
               "Cache-Control": "max-age=0", "Connection": "keep-alive",
               "Content-Length": "206", "Content-Type": "application/x-www-form-urlencoded",
               "Cookie": "UM_distinctid=15d2f3332fc3c0-09042104ddbf9-8383667-1fa400-15d2f3332fd24d; Hm_lvt_cdb4bc83287f8c1282df45ed61c4eac9=1499735471,1500601585; JSESSIONID=VDgyZ2qDjq6c1k6KFKh07zcqkpnhDfwV3mVLfLwyjx3Y1Jv0hMhJ!-699126804; CNZZDATA1256107480=538513944-1500267535-http%253A%252F%252Fsn.gsxt.gov.cn%252F%7C1500947649",
               "Host": "sn.gsxt.gov.cn", "Origin": "http://sn.gsxt.gov.cn",
               "Referer": "http://sn.gsxt.gov.cn/xxcx.do?method=xxggList&xxlx=1&status=2&random=1500949143643",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}

    def start_requests(self):
        param = {"method": "xxggList", "random": str(self.timstamp), "xxlx": "1", "status": "2", "djjg": "", "entname": "",
                 "xh": "",
                 "glxh": "", "geetest_challenge": "", "geetest_validate": "", "geetest_seccode": "",
                 "page.currentPageNo": "1"}

        url_page = 'http://sn.gsxt.gov.cn/xxcx.do'
        r = requests.post(url_page, data=param, headers=self.headers_list)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        total_pages = int(soup.find_all('div', {"class": "page"})[0].find_all(class_='number')[1].get_text(strip=True))

        # print('total pages:%s' % total_pages)
        for i in range(1,total_pages):
            url = 'http://sn.gsxt.gov.cn/xxcx.do'
            yield scrapy.FormRequest(url=url,formdata={"method": "xxggList", "random": str(self.timstamp), "xxlx": "1", "status": "2", "djjg": "", "entname": "",
             "xh": "",
             "glxh": "", "geetest_challenge": "", "geetest_validate": "", "geetest_seccode": "",
             "page.currentPageNo": str(i)})


    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content,"lxml")
        tag_ul = soup.find_all(class_='xxgg_list')
        tag_li = tag_ul[0].find_all('li')
        for each in tag_li:
            title = each.find_all('a')[0].get_text(strip=True)
            para_list = each.find_all('a')[0]['onclick'].encode('utf-8').split(',')
            number1 = para_list[2].replace('\'', '')
            number2 = para_list[3].replace('\'', '').replace(');', '')
            pun_org = each.find_all(class_='depar')[0]['title']
            pun_date = each.find_all(class_='date')[0]['title']
            ent_name = each.find_all('a')[0].get_text(strip=True).replace(u'关于', '').replace(u'企业列入经营异常名录公告', '')

            url_detail = 'http://sn.gsxt.gov.cn/xxcx.do'

            self.count = self.count + 1

            yield scrapy.FormRequest(url=url_detail,formdata={"method": "xxggXq", "random": "1500282496884", "xxlx": "1", "status": "2", "djjg": "", "entname": "",
             "xh": str(number1),
             "glxh": str(number2), "geetest_challenge": "", "geetest_validate": "", "geetest_seccode": "",
             "currentPageNo": "1"},meta={"pun_org": pun_org,"pun_date": pun_date,"ent_name": ent_name},callback=self.parse_detail)

    def parse_detail(self,response):
        item = crawler114()
        content = response.body
        soup = BeautifulSoup(content,"lxml")

        # try:
        #     case_no = soup.find_all('p')[2].get_text(strip=True)
        # except:
        #     case_no = None
        #
        # try:
        #     pun_reason = soup.find_all('p')[4].get_text(strip=True)
        # except:
        #     pun_reason = None
        try:
            case_no = response.xpath('''/html/body/form/div[1]/div[4]/div/div/div/div[2]/div/div/p[2]/text()''')[0].extract()
        except:
            case_no = None

        try:
            pun_reason = response.xpath('''/html/body/form/div[1]/div[4]/div/div/div/div[2]/div/div/p[4]/text()''')[0].extract()
        except:
            pun_reason = None
        data_source = 'crawler114_8'
        del_flag = '0'
        op_flag = 'a'
        create_date = time.strftime('%Y-%m-%d', time.localtime())

        item['case_no'] = case_no
        item['punish_org'] = response.meta['pun_org']
        item['punish_date'] = response.meta['pun_date']
        item['entity_name'] = response.meta['ent_name']
        item['punish_reason'] = pun_reason
        item['data_source'] = data_source
        item['del_flag'] = del_flag
        item['op_flag'] = op_flag
        item['create_date'] = create_date
        item['source_url'] = response.url
        item['source_page'] = content
        item['data_id'] = 'shanxi'
        item['spider_name'] = self.name

        yield item

