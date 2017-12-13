# -*- coding: utf-8 -*-
import requests
import scrapy


class Crawler001Spider(scrapy.Spider):
    name = 'crawler001'
    allowed_domains = ['http://naxy.moa.gov.cn']
    headers = {"Accept":"application/json, text/javascript, */*; q=0.01","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9","Connection":"keep-alive","Content-Length":"84","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Cookie":"JSESSIONID=CgIFVgBQWijwOb_QkvGwrEmZjllr9mPx2qAA; _gscs_1951462215=126323666e1yk118|pv:2; _gscbrs_1951462215=1; _gscs_20481343=1263236894e2sk15|pv:2; _gscbrs_20481343=1; _gscu_20481343=11514330ych2q015; _gscu_1951462215=11514326wvowfx20","Host":"naxy.moa.gov.cn","Origin":"http://naxy.moa.gov.cn","Referer":"http://naxy.moa.gov.cn/naxy/punish/gfsx","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36","X-Requested-With":"XMLHttpRequest","X-Tingyun-Id":"p35OnrDoP8k;r=32384979"}

    def start_requests(self):
        url_page = 'http://naxy.moa.gov.cn/naxy/punish/listGfsx'
        param = {"publicflag":"1","_search":"false","nd":"1512632384973","pageSize":"10","pageNo":"1","orderFields":"","order":""}
        r = requests.post(url=url_page,headers=self.headers,data=param)
        json_content = r.json()
        total_pages = int(json_content['total'])
        print(total_pages)

        for i in range(1,3):
            url = 'http://naxy.moa.gov.cn/naxy/punish/listGfsx'
            yield scrapy.FormRequest(url=url,headers=self.headers,formdata={"publicflag":"1","_search":"false","nd":"1512632384973","pageSize":"10","pageNo":str(i),"orderFields":"","order":""})



    def parse(self, response):
        pass
