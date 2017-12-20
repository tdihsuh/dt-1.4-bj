# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy_migrate_project.items import C008Item
import time
import re



class C008Spider(scrapy.Spider):
    name = 'c008'
    allowed_domains = ['hd.chinatax.gov.cn']
    url = 'http://hd.chinatax.gov.cn/xxk/action/ListXxk.do'
    root='http://hd.chinatax.gov.cn/xxk/action/'
    param = {'categeryid': '24',
             'querystring24': 'articlefield02',
             'querystring25': 'articlefield02',
             'queryvalue': '',
                }
    def start_requests(self):
        yield scrapy.FormRequest(self.url,
                                 formdata=self.param,
                                 dont_filter=True
                                 )


    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        list = soup.find_all('td')
        temp = list[0].get_text(strip=True)
        slip = temp.split('/')
        pagestr = slip[-1]
        # print(page.decode('utf-8'))
        totalpages = int(re.search(r'\d+',pagestr).group(0))
        # print(totalpages,type(totalpages))
        for page in range(1,1+totalpages):
            self.param['cPage']=str(page)
            yield scrapy.FormRequest(self.url,
                                     formdata=self.param,
                                     callback=self.getDetailUrl,
                                     dont_filter=True,
                                     meta={'page':page}
                                     )
    def getDetailUrl(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        table = soup.find_all('table')[1]
        td=table.find_all('td')[1:]


        for each in range(len(td)):

            cname = td[each].get_text(strip=True)
            # print(response.meta['page'],u'页',cname)
            clink = td[each].a.attrs['href']
            yield scrapy.Request(self.root+clink,callback=self.parseDetail)

    def parseDetail(self,response):
        soup2=BeautifulSoup(response.text,'lxml')
        tb2 = soup2.find_all('table')[1].find_all('tr')
        # print len(tb)
        t_m0 = tb2[0].find_all('td')
        taxName = t_m0[1].get_text(strip=True)

        t_m1 = tb2[1].find_all('td')
        taxNum = t_m1[1].get_text(strip=True)

        t_m2 = tb2[2].find_all('td')
        orgNum = t_m2[1].get_text(strip=True)

        t_m3 = tb2[3].find_all('td')
        regAddress = t_m3[1].get_text(strip=True)

        t_m4 = tb2[4].find_all('td')

        legalMan = t_m4[1].get_text(strip=True)
        detail = legalMan.split(',')
        legalManName = detail[0]
        legalManSex = u'男' if u'男' in legalMan else u'女'
        legalManidentifyNum = re.search(r'\w*\*+\w*',legalMan).group(0) if re.search(r'\w*\*+\w*',legalMan) else legalMan

        t_m5 = tb2[-1].find_all('td')
        uncreditContent = t_m5[1].get_text(strip=True)

        t_m6 = tb2[-2].find_all('td')
        caseNature = t_m6[1].get_text(strip=True)
        item=C008Item()

        item['tax_name'] = taxName
        item['tax_num'] = taxNum
        item['org_num']= orgNum
        item['reg_address'] = regAddress

        item['legal_man_name'] = legalManName
        item['legal_man_sex'] = legalManSex
        item['legal_man_identify_num'] = legalManidentifyNum
        item['case_nature'] = caseNature
        item['uncredit_content'] = uncreditContent
        item['create_date'] =time.strftime('%Y-%m-%d', time.localtime())

        item['source_page']= response.text
        item['source_url']=response.url
        item['spider_name']=self.name
        yield item






