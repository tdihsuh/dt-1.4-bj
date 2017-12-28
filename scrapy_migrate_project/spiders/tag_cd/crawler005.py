# -*- coding: utf-8 -*-
import urllib2

import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler005


class Crawler005Spider(scrapy.Spider):
    name = 'crawler005'
    allowed_domains = ['www.bcpcn.com']
    # start_urls = ['http://www.bcpcn.com/']

    def start_requests(self):
        paggee = 1
        url = 'http://www.bcpcn.com/gfthhbanglist?&sid=141&rn=15&pn=' + str(paggee)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        a = soup.find_all(class_='hei_left_bottom')
        totalitemsstr = a[0].get_text(strip=True).encode('utf-8')
        totalitems = filter(str.isalnum, totalitemsstr)
        totalitems = int(totalitems)

        if totalitems % 15 == 0:
            totalpages = totalitems / 15
        else:
            totalpages = totalitems // 15 + 1

        for i in range(1,2):
            url = 'http://www.bcpcn.com/gfthhbanglist?&sid=141&rn=15&pn=' + str(i)

            yield scrapy.Request(url=url)



    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, "lxml")
        a = soup.find_all(class_='hei_left_middle')
        p = a[0].ul.find_all('li')
        for j in range(len(p)):
            ppp = p[j].find_all('span')
            link1 = ppp[1].a['href']

            yield scrapy.Request(url=link1,callback=self.parse_detail)


    def parse_detail(self,response):
        html = response.body
        soup = BeautifulSoup(html, "lxml")

        detail = soup.find_all(class_='hongbang_body heibang_body')
        detail1 = detail[0].ul.find_all('li')

        item = crawler005()

        # 以下为字段解析
        detaildic = {}
        for jj in range(len(detail1)):

            try:
                detail1[jj]['class']
            except:
                colonLeft = detail1[jj].span.get_text(strip=True)
                colonRight = detail1[jj].get_text(strip=True).replace(colonLeft, '')
                colonLeft1 = colonLeft[:-1]
                detaildic[colonLeft1] = colonRight
        punishType = None
        punishDate = None
        punishDepartment = None
        fileNum = None
        compName = None
        socialUnionNum = None
        businessRegNum = None
        fianceNum = None
        legalMan = None
        deadLine = None
        orgNum = None
        regAddress = None
        managerRange = None
        if detaildic.has_key(unicode('处罚类型', 'utf8')):
            punishType = detaildic[unicode('处罚类型', 'utf8')].replace(' ', '')
            # print punishType

        if detaildic.has_key(unicode('处罚日期', 'utf8')):
            punishDate = detaildic[unicode('处罚日期', 'utf8')].replace(' ', '')
            # print '处罚日期'

        if detaildic.has_key(unicode('处罚机构', 'utf8')):
            # print '处罚机构'
            punishDepartment = detaildic[unicode('处罚机构', 'utf8')].replace(' ', '')
            # print punishDepartment

        if detaildic.has_key(unicode('文件号', 'utf8')):
            fileNum = detaildic[unicode('文件号', 'utf8')].replace(' ', '')
            # print fileNum

        if detaildic.has_key(unicode('企业名称', 'utf8')):
            compName = detaildic[unicode('企业名称', 'utf8')].replace(' ', '')
            # print compName

        if detaildic.has_key(unicode('社会统一代码', 'utf8')):
            socialUnionNum = detaildic[unicode('社会统一代码', 'utf8')].replace(' ', '')
            # print socialUnionNum

        if detaildic.has_key(unicode('工商注册号', 'utf8')):
            businessRegNum = detaildic[unicode('工商注册号', 'utf8')].replace(' ', '')
            # print businessRegNum

        if detaildic.has_key(unicode('经济类型', 'utf8')):
            fianceNum = detaildic[unicode('经济类型', 'utf8')].replace(' ', '')
            # print fianceNum

        if detaildic.has_key(unicode('法定代表人', 'utf8')):
            legalMan = detaildic[unicode('法定代表人', 'utf8')].replace(' ', '')
            # print legalMan

        if detaildic.has_key(unicode('营业期限', 'utf8')):
            deadLine = detaildic[unicode('营业期限', 'utf8')].replace(' ', '')
            # print deadLine

        if detaildic.has_key(unicode('组织机构代码', 'utf8')):
            orgNum = detaildic[unicode('组织机构代码', 'utf8')].replace(' ', '')
            # print orgNum

        if detaildic.has_key(unicode('注册地址', 'utf8')):
            regAddress = detaildic[unicode('注册地址', 'utf8')].replace(' ', '')
            # print regAddress

        if detaildic.has_key(unicode('经营范围', 'utf8')):
            managerRange = detaildic[unicode('经营范围', 'utf8')].replace(' ', '')
            # print managerRange

        create_date = time.strftime('%Y-%m-%d', time.localtime())
        item['punishType'] = punishType
        item['punishDate'] = punishDate
        item['punishDepartment'] = punishDepartment
        item['fileNum'] = fileNum
        item['compName'] = compName
        item['socialUnionNum'] = socialUnionNum
        item['businessRegNum'] = businessRegNum
        item['fianceNum'] = fianceNum
        item['legalMan'] = legalMan
        item['deadLine'] = deadLine
        item['orgNum'] = orgNum
        item['regAddress'] = regAddress
        item['managerRange'] = managerRange
        item['source_url'] = response.url
        # item['source_page'] = html
        item['spider_name'] = self.name

        yield item




