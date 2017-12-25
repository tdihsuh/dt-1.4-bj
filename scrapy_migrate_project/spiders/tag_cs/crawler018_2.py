# -*- coding: utf-8 -*-
# "采集证监会市场禁入处罚信息"
import scrapy
import re
import time
import scrapy
from scrapy_migrate_project.items import Crawler018Item
from bs4 import BeautifulSoup



class ZjhShichangSpider(scrapy.Spider):
    name = 'crawler018_2'
    allowed_domains = ['csrc.gov.cn']
    start_urls = ['http://www.csrc.gov.cn/wcm/govsearch/year_gkml_list.jsp?page=1&schn=3619&sinfo=3300&countpos=1']


    # 列表页
    def parse(self, response):
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        tag = soup.find(name='div', id='documentContainer')

        # 提取每个链接的详细信息，逐条下载
        nodes = tag.find_all(name='div', class_='row')

        for node in (nodes):
            # 获取处罚标题、发文日期、文号和链接
            item = Crawler018Item()
            hnode = node.find(class_='mc').div.a
            item['title'] = hnode.text
            link = hnode.get('href')
            link = 'http://www.csrc.gov.cn'+link
            item['pub_date']= node.find(class_='fbrq').text
            item['case_no'] = node.find(class_='wh').text
            yield scrapy.Request(link,
                                  callback=self.parse_detail,
                                  meta={'item': item}
                                  )
        total_num = re.findall("var m_nRecordCount = (.*?);", data)
        total_num = [i for i in total_num if len(i) > 2][0]

        # 之后的请求是post请求，在变的是page，从2到最后一页，page的数字和当前的页码数相同
        # 取整之后如果有刚好被20整除那么就是(int(total_num)//20)+2-1 #往后移动2并且减掉第一页
        # 取整之后如果不能被20整除那么就是(int(total_num)//20)+1+2-1 #加上最后一页，往后移动2并且减掉第一页
        final_page_num = (int(total_num) // 20) + 1 + 2 - 1 if int(total_num) % 20 != 0 else (int(
            total_num) // 20) + 2 - 1
        for i in range(2, final_page_num):
            url = "http://www.csrc.gov.cn/wcm/govsearch/year_gkml_list.jsp"
            post_data = {
                "page": str(i),
                "schn": "3619",
                "sinfo": "3300",
                "years": "",
                "countpos": "1",
                "curpos": ""
            }
            yield scrapy.FormRequest(
                url,
                formdata=post_data,
                callback=self.parse
            )
    # 详情页
    def parse_detail(self, response):
        item = response.meta['item']
        data = response.text
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        item['source_page'] = data
        soup = BeautifulSoup(data, "lxml")
        main_node = soup.find(name='div', class_='content')
        item['content'] = main_node.text.encode('utf-8').strip()

        # 从header中提取最后Last-modified信息
        last_modified = response.headers['Last-modified']
        if (last_modified == None or len(last_modified) == 0):
            last_modified = response.headers['If-Modified-Since']

        hashcode = hash(response.url + last_modified)

        # if check_history(hashcode):
        #     pass
        # else:
        # 提取数据
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())

        tmp_node = main_node.div

        pnodes = main_node

        if tmp_node == None:
            pnodes = main_node.find_all(name='p')
        else:
            pnodes = tmp_node.find_all(name='p')

        human = []
        gender = []
        memo = []

        for pnode in pnodes:
            # 提取被处罚个人信息
            node_text = pnode.text.encode('utf-8')

            # 个人信息特征，男/女、出生，住址：
            if ((node_text.find('男') != -1 or node_text.find('女') != -1) and node_text.find(
                    '出生，') != -1 and node_text.find('住址：') != -1):
                # 提取姓名
                item['person_name'] = self.get_person_name(node_text)
                human.append(item['person_name'])
                # 提取性别
                gender_flag = self.get_gender(node_text)
                gender.append(gender_flag)
                item['gender'] = gender
                # 提取个人备注信息
                person_memo = self.get_person_memo(node_text)
                memo.append(person_memo)
                item['memo'] = memo

            else:
                pass
        item['org_level'] = '1'
        yield item

    def get_person_name(self, content):
        person_name = ''
        if content.find('当事人') != -1:
            person_name = content[0:content.find('，')].replace('当事人：', '')
        else:
            person_name = content[0:content.find('，')]
        return person_name.strip()

    def get_person_memo(self, content):
        regex = re.compile(r"，(.*)。")
        if content.find('，男，') != -1:
            regex = re.compile(r"男，(.*)。")
        elif content.find('，女，'):
            regex = re.compile(r"女，(.*)。")
        else:
            pass

        results = regex.findall(content)
        if len(results) > 0:
            return results[0].strip()
        else:
            return None

    def get_gender(self, content):
        if content.find('，男，') != -1:
            return '男'
        elif content.find('，女，'):
            return '女'
        else:
            return '未知'

