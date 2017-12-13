# -*- coding: utf-8 -*-
import requests
import scrapy
import time
from bs4 import BeautifulSoup

from scrapy_migrate_project.items import crawler007


class Crawler007Spider(scrapy.Spider):
    name = 'crawler007'
    allowed_domains = ['www.ccgp.gov.cn']

    def start_requests(self):
        param = {'orgName': '', 'enforceUnit': '', 'punishTime': '', 'punishTimeMax': '', 'gp': '1'}
        r = requests.post("http://www.ccgp.gov.cn/cr/list", data=param)
        soup = BeautifulSoup(r.text, "lxml")

        pagelist = soup.find_all(id='totalPag')
        pagestr = pagelist[0].get_text(strip=True)
        total_pages = int(pagestr)

        for i in range(1,total_pages):
            url = 'http://www.ccgp.gov.cn/cr/list'
            yield scrapy.FormRequest(url=url,formdata={'orgName': '', 'enforceUnit': '', 'punishTime': '', 'punishTimeMax': '', 'gp': str(i)})

    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content, "lxml")
        list = soup.find_all(class_='trShow')

        item = crawler007()

        for i in range(len(list)):
            itemSet = list[i].find_all('td')
            num = itemSet[0].get_text(strip=True)
            companyName = itemSet[1].get_text(strip=True)
            orgNum = itemSet[2].get_text(strip=True)
            compAddress = itemSet[3].get_text(strip=True)
            uncreditContent = itemSet[4].p['title'].replace(' ', '')
            punishResult = itemSet[5].p['title'].replace(' ', '')
            punishBy = itemSet[6].p['title'].replace(' ', '')
            punishDate = itemSet[7].get_text(strip=True)
            exeDepartment = itemSet[8].get_text(strip=True)
            create_date = time.strftime('%Y-%m-%d', time.localtime())

            item['companyName'] = companyName
            item['orgNum'] = orgNum
            item['compAddress'] = compAddress
            item['uncreditContent'] = uncreditContent
            item['punishResult'] = punishResult
            item['punishBy'] = punishBy
            item['punishDate'] = punishDate
            item['exeDepartment'] = exeDepartment
            item['create_date'] = create_date
            item['source_url'] = response.url
            item['source_page'] = content

            yield item

