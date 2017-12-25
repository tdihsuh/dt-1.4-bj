# -*- coding: utf-8 -*-
# 采集国家食药监局的药品飞行检查数据，只处理3种格式化网页的数据抓取
import re

import scrapy
import time
from bs4 import BeautifulSoup
from scrapy_migrate_project.items import Crawler015Item


class GovMedicineSpider(scrapy.Spider):
    name = 'crawler015'
    allowed_domains = ['sfda.gov.cn']
    start_urls = ['http://www.sfda.gov.cn/WS01/CL1850/index.html']

    # 列表页
    def parse(self, response):
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        tag = soup.find(name='td', class_='2016_erji_content').contents[0]

        # 提取每个链接的详细信息，逐条下载
        href_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        hrefs = href_regex.findall(str(tag))
        for href in (hrefs):
            link = 'http://www.sfda.gov.cn/WS01/' + href
            link = link.replace('../','')
            yield scrapy.Request(link,
                                 callback=self.parse_detail)
        # 翻页
            # 总页数
        tag = soup.find(class_='pageTdSTR15')
        page_num = 1
        page_str = tag.text.encode('utf-8').split('/')  # 第1页/共5页
        pattern = re.compile(r'[0-9]+')
        match = re.search(pattern, page_str[1])
        if match:
            page_num = int(match.group())

        for i in range(1, page_num, 1):
            url = 'http://www.sfda.gov.cn/WS01/CL1850/index_'+str(i)+'.html'
            yield scrapy.Request(url,
                                 callback=self.parse)

    # 详情页
    def parse_detail(self, response):
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        item = Crawler015Item()
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        item['source_page'] = data
        # 从header中提取最后Last-modified信息
        last_modified = response.headers['Last-modified']
        if (last_modified == None or len(last_modified) == 0):
            last_modified = response.headers['If-Modified-Since']

        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        item['title'] = soup.find(name='td', class_='articletitle3').text

        tag = soup.find(name='td', class_='articlecontent3')

        # 模板1：页面信息中包含“社会信用代码、企业法定代表人”标题
        # 模板2：页面信息中包含“企业名称、存在的主要问题、处理情况、备注”标题
        node1 = tag.find(text='社会信用代码')
        node2 = tag.find(text='企业法定代表人')
        if (node1 != None and node2 != None):
            # 按照模板1提取详细信息
            trnodes = tag.table.tbody.contents

            tdnodes0 = trnodes[0].contents
            item['ent_name'] = tdnodes0[1].text
            item['legal_man'] = tdnodes0[3].text

            tdnodes1 = trnodes[1].contents
            item['medicine_certno'] = tdnodes1[1].text
            item['credit_code'] = tdnodes1[3].text

            tdnodes4 = trnodes[4].contents
            item['address'] = tdnodes4[1].text

            tdnodes5 = trnodes[5].contents
            item['check_date'] = tdnodes5[1].text

            tdnodes6 = trnodes[6].contents
            item['check_org'] = tdnodes6[1].text.encode('utf-8').replace('核查中心', ' ', 1)

            if len(trnodes) == 12:
                tdnodes8 = trnodes[8].contents
                item['problem'] = tdnodes8[0].text

                tdnodes10 = trnodes[10].contents
                item['operation'] = tdnodes10[0].text

                tdnodes11 = trnodes[11].contents
                item['pub_date'] = tdnodes11[1].text

            elif len(trnodes) == 11:
                tdnodes5 = trnodes[5].contents
                item['check_date'] = tdnodes5[3].text

                tdnodes8 = trnodes[8].contents
                item['problem'] = tdnodes8[0].text

                tdnodes10 = trnodes[10].contents
                item['operation'] = tdnodes10[0].text

                pub_date = soup.find(name='td', class_='articletddate3').text.encode('utf-8')
                item['pub_date'] = pub_date.replace(' 发布', '')

            else:
                tdnodes7 = trnodes[7].contents
                item['check_reason'] = tdnodes7[1].text

                tdnodes9 = trnodes[9].contents
                item['problem'] = tdnodes9[0].text

                tdnodes11 = trnodes[11].contents
                item['operation'] = tdnodes11[0].text

                tdnodes12 = trnodes[12].contents
                item['pub_date'] = tdnodes12[1].text
            item['pub_mode'] = '1'
        else:
            node1 = tag.find(text='企业名称')
            node2 = tag.find(text='存在的主要问题')
            node3 = tag.find(text='处理情况')
            node4 = tag.find(text='备注')

            if (node1!=None and node2!=None and node3!=None and node4!=None):
                # 按照模板2提取详细信息
                trnodes = tag.table.tbody.contents
                trnodes = tag.find(name='tbody').contents

                for i in range(1,len(trnodes),1):
                    tdnodes = trnodes[i].contents
                    item['ent_name'] = tdnodes[0].text
                    item['problem'] = tdnodes[1].text
                    item['operation'] = tdnodes[2].text
                    memo = tdnodes[3].text
                    pub_date = soup.find(name='td', class_='articletddate3').text.encode('utf-8')
                    item['pub_date'] = pub_date.replace(' 发布','')
                    item['pub_mode']='2'

            elif item['title'].find('GMP')==-1: #不属于模板1和模板2的页面格式，直接保存文本

                pub_date = soup.find(name='td', class_='articletddate3').text.encode('utf-8')
                item['pub_date'] = pub_date.replace(' 发布', '')
                item['operation'] = soup.find(name='td', class_='articlecontent3').text

                #从标题中提取企业名称
                title = item['title'].encode('utf-8')
                start = title.find('对')
                mid = title.find('公司')
                end = title.find('飞行检查')
                if (start==-1 or mid==-1 or end==-1):
                    pass
                else:
                    item['ent_name'] = title[start+3:mid+6]

                item['pub_mode'] = '3'
        yield item

