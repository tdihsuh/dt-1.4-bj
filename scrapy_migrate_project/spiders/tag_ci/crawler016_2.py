# -*- coding: utf-8 -*-
# 采集保监局行政处罚信息
import re
import sys
import scrapy
import time

from scrapy_migrate_project.items import Crawler016Item
from bs4 import BeautifulSoup
from bs4.element import Tag
reload(sys)
sys.setdefaultencoding('utf8')


class BjjXingzhengSpider(scrapy.Spider):
    name = 'crawler016_2'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://www.circ.gov.cn/web/site0/tab5241/module14458/page1.htm']

    # 列表页
    def parse(self, response):
        li_list = response.xpath('//td[@class="hui14"]')
        for li in li_list:
            item = Crawler016Item()
            title = li.xpath('./span/a/text()').extract_first()
            # 根据title提取处罚书文号，文号必须包括‘保监罚’字眼
            if (title.find('处罚决定书') != -1 and title.find('保监罚') != -1):
                case_no = title[title.find('处罚决定书'):len(title)].replace('处罚决定书', '').replace('—', '').strip()
            else:
                case_no = title
            if (case_no != None and len(case_no) > 200):
                case_no = case_no[0:200]
            item['case_no'] = case_no
            item['title'] = title
            href = li.xpath('./span/a/@href').extract_first()
            href = 'http://www.circ.gov.cn'+ href
            pub_date =li.xpath('./following-sibling::*[1]/text()').extract_first()
            pub_date ='20' + pub_date.replace(')', '').replace('(', '')
            item['pub_date'] = pub_date
            yield scrapy.Request(href,
                                 callback=self.parse_detail,
                                 meta={'item':item})

        # 翻页
        ret = response.xpath('//td[@class="Normal"]/text()').extract()
        cur_page = response.xpath('//td[@class="Normal"]/font/text()').extract_first()
        total_pages = ret[-1].split('/')[-1]
        if int(cur_page) < int(total_pages):
            next_page = int(cur_page)+1
            next_url = 'http://www.circ.gov.cn/web/site0/tab5241/module14458/page'+str(next_page)+'.htm'
            yield scrapy.Request(next_url,
                                 callback=self.parse)
    #详情页
    def parse_detail(self,response):
        item = response.meta['item']
        title= item['title']
        data = response.text
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        item['source_page'] = data
        soup = BeautifulSoup(data, "lxml")

        # 提取数据
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())

        # 提取处罚内容
        node = soup.find(name='span', class_='xilanwb')
        item['content'] = node.text.encode('utf-8').strip()

        # 提取公司名称
        subnodes = node.children

        ent_name = ''

        for subnode in (subnodes):
            if isinstance(subnode, Tag):  # 提取每行信息
                node_text = subnode.text.encode('utf-8').replace(' ', '').strip()
                if (node_text.startswith('当事人：') or node_text.startswith('当事人名称：') or node_text.startswith(
                        '受处罚机构：') or node_text.startswith('受处罚机构名称：') or node_text.startswith(
                        '受处罚单位：') or node_text.startswith('受处罚单位名称：') or node_text.startswith(
                        '受处罚人：') or node_text.startswith('受罚人：') or node_text.startswith(
                        '受处罚人名称：') or node_text.startswith('名称：') or node_text.startswith(
                        '机构名称：') or node_text.startswith('被处罚机构名称：')):

                    if (node_text.find('以下简称') != -1 and node_text.find('公司') != -1):  # 先确定是否是企业信息
                        ent_name = self.get_ent_content(node_text[node_text.find('：'):len(node_text)].replace('：', ''))
                        # 去掉（简称）字眼
                        regex = re.compile(r"（(.*)）")
                        results = regex.findall(ent_name)
                        if (results != None and len(results) > 0):
                            result = '（' + results[0] + '）'
                            ent_name = ent_name.replace(result, '')
                    elif node_text.find('公司') != -1:  # 先确定是否是企业信息
                        ent_name = self.get_ent_content(node_text[node_text.find('：'):len(node_text)].replace('：', ''))
                    else:
                        pass
                    ent_name = ent_name.strip()
        item['ent_name'] = ent_name
        item['org_level'] = '2'
        yield item

    def get_ent_content(self,content):  # 截取字符串,如果发现，。需要进行截取
        result = None
        if (content != None):
            if content.find('。') != -1:
                result = content[0:content.find('。')]
            elif content.find('，') != -1:
                result = content[0:content.find('，')]
            else:
                result = content
        return result


