# -*- coding: utf-8 -*-
# 采集保监会行政处罚信息
import re

import scrapy
import time
from bs4 import BeautifulSoup
from bs4.element import Tag
from scrapy_migrate_project.items import Crawler016Item
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class BjhXingzhengSpider(scrapy.Spider):
    name = 'crawler016'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://www.circ.gov.cn/web/site0/tab5240/module14430/page1.htm']

    # 列表页
    def parse(self, response):
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        tag = soup.find(name='table', id='ess_ctr14430_ListC_Info_LstC_Info')

        # 提取每个链接的详细信息，逐条下载
        nodes = tag.find_all(name='td', class_='hui14')
        for node in (nodes):
            item = Crawler016Item()
            title = node.text.encode('utf-8')
            item['title'] = title
            if (title.find('中国保险监督管理委员会行政处罚决定书') != -1):
                href_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
                hrefs = href_regex.findall(str(node))[0]
                link = 'http://www.circ.gov.cn'+hrefs
                pubnode = node.parent.contents

                item['pub_date'] = '20' + pubnode[5].text.encode('utf-8').replace(')', '').replace('(', '')
                yield scrapy.Request(link,
                                     callback=self.parse_detail,
                                     meta={'item':item})
        # 翻页
        url = response.url
        ret = url.split('/')[-1]
        cur_page = int(re.findall(r'\w+(\d+).*?', ret)[0])
         # 提取总页数
        tag = soup.find(id='ess_ctr14430_ListC_Info_AspNetPager')
        # node1 = tag.find(name='td', class_='Normal')
        page_str = tag.text.encode('utf-8').split('/')  # 第1页/共5页
        pattern = re.compile(r'[0-9]+')
        match = re.search(pattern, page_str[1])
        if match:
            page_num = int(match.group())

        # 抓取其它页面数据
        if cur_page < page_num:
            cur_page += 1
            url = 'http://www.circ.gov.cn/web/site0/tab5240/module14430/page' +str(cur_page) + '.htm'
            yield scrapy.Request(url,
                                 callback=self.parse
                                 )

    # 详情页
    def parse_detail(self, response):
        item = response.meta['item']
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        data = response.text
        item['source_page'] = data
        total_num = re.findall("var m_nRecordCount = (.*?);", data)
        soup = BeautifulSoup(data, "lxml")
        # 提取数据
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())

        # 提取处罚文书编号、处罚内容
        title = item['title']
        item['case_no'] = title.replace('中国保险监督管理委员会行政处罚决定书', '').replace('（', '').replace('）', '')

        node = soup.find(name='span', class_='xilanwb')
        if node:
            item['content'] = node.text

        # 提取公司名称、自然人当事人姓名和身份证号码
        human = []
        idcard = []
        address = []
        item['org_level'] = '1'
        if node:
            subnodes = node.children
            for subnode in (subnodes):

                if isinstance(subnode,Tag):#提取每行信息
                    node_text = subnode.text.encode('utf-8')
                    if node_text.find('当事人：')!=-1:
                        if (node_text.find('，')==-1 and node_text.find('公司')!=-1):#先确定是否是企业信息
                            ent_name=self.get_substr(node_text,'当事人：').strip()
                            #去掉（简称）字眼
                            regex = re.compile(r"（(.*)）")
                            results = regex.findall(ent_name)
                            if (results!=None and len(results)>0):
                                result = '（' + results[0] + '）'
                                item['ent_name'] = ent_name.replace(result, '')
                        elif (node_text.find('以下简称')!=-1 and node_text.find('公司')!=-1):#先确定是否是企业信息
                            ent_name=self.get_substr(node_text,'当事人：').strip()
                            #去掉（简称）字眼
                            regex = re.compile(r"（(.*)）")
                            results = regex.findall(ent_name)
                            if (results!=None and len(results)>0):
                                result = '（' + results[0] + '）'
                                item['ent_name'] = ent_name.replace(result, '')
                        else:
                            human.append(self.get_substr(node_text, '当事人：').strip())

                    if node_text.find('当事人:')!=-1:
                        if (node_text.find('，')==-1 and node_text.find('公司')!=-1):#先确定是否是企业信息
                            ent_name=self.get_substr(node_text,'当事人:').strip()
                            #去掉（简称）字眼
                            regex = re.compile(r"（(.*)）")
                            results = regex.findall(ent_name)
                            if (results!=None and len(results)>0):
                                result = '（' + results[0] + '）'
                                item['ent_name'] = ent_name.replace(result, '')
                        elif (node_text.find('以下简称')!=-1 and node_text.find('公司')!=-1):#先确定是否是企业信息
                            ent_name=self.get_substr(node_text,'当事人:').strip()
                            #去掉（简称）字眼
                            regex = re.compile(r"（(.*)）")
                            results = regex.findall(ent_name)
                            if (results!=None and len(results)>0):
                                result = '（' + results[0] + '）'
                                item['ent_name'] = ent_name.replace(result, '')
                        else:
                            human.append(self.get_substr(node_text, '当事人:').strip())


                    if node_text.find('身份证号：') != -1:
                        idcard.append(self.get_substr(node_text, '身份证号：').strip())
                    if node_text.find('身份证号:') != -1:
                        idcard.append(self.get_substr(node_text, '身份证号:').strip())

                    if node_text.find('护照号：') != -1:
                        idcard.append(self.get_substr(node_text, '护照号：').strip())
                    if node_text.find('护照号:') != -1:
                        idcard.append(self.get_substr(node_text, '护照号:').strip())

                    if node_text.find('住址：') != -1:
                        address.append(self.get_substr(node_text, '住址：').strip())
                    if node_text.find('住址:') != -1:
                        address.append(self.get_substr(node_text, '住址:').strip())

        yield item

    def get_substr(self, content, key):  # 截取字符串,如果发现，。需要进行截取
        if (content != None and content.find(key) != -1):
            result = content[content.find(key):len(content)].replace(key, '')
            if result.find('。') != -1:
                result = result[0:result.find('。')]
            if result.find('，') != -1:
                result = result[0:result.find('，')]
            return result

        else:
            return None