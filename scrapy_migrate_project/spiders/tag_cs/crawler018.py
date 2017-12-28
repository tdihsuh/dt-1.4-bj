# -*- coding: utf-8 -*-
# "采集证监会行政处罚信息"
import re
import sys,time
from bs4 import BeautifulSoup
import scrapy
from scrapy_migrate_project.items import Crawler018Item
from selenium import webdriver
# from cycredit.SysConfig import SysConfig as sysconfig
# from cycredit.SysLog import SysLog as logger
# from cycredit.RedisUtil import RedisUtil as


class JzhXingzhengSpider(scrapy.Spider):
    name = 'crawler018'
    allowed_domains = ['csrc.gov.cn']
    start_urls = ['http://www.csrc.gov.cn/wcm/govsearch/year_gkml_list.jsp?page=1&schn=3313&sinfo=3300&countpos=1']

    # 检查下载历史
    # def check_history(hashcode):
    #     return redis.hexists('crawler018', hashcode)

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
        # 翻页
        driver = webdriver.PhantomJS(executable_path=sysconfig.get_field('phantomjs', 'path'))
        driver.get(response.url)
        time.sleep(3)


        page_node = driver.find_element_by_id('list_navigator')
        current_num = int(
            page_node.find_element_by_class_name('nav_currpage').get_attribute('innerHTML').encode('utf-8'))
        page_num = int(page_node.find_element_by_class_name('nav_page_detail').find_element_by_class_name(
            'nav_pagenum').get_attribute('innerHTML').encode('utf-8'))
        driver.quit()

        if current_num < page_num:
            i = current_num + 1
            url = 'http://www.csrc.gov.cn/wcm/govsearch/year_gkml_list.jsp?page=' + str(
                i) + '&schn=3619&sinfo=3300&countpos=1'
            yield scrapy.Request(url,
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

        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        tmp_node = main_node.div

        pnodes = main_node

        if tmp_node == None:
            pnodes = main_node.find_all(name='p')
        else:
            pnodes = tmp_node.find_all(name='p')

        ent_name = ''
        human = []
        gender = []
        memo = []

        for pnode in (pnodes):
            # 提取被处罚个人和企业信息
            node_text = pnode.text.encode('utf-8')
            # 企业信息特征，当事人、公司、住所：
            if (node_text.find('当事人') != -1 and node_text.find('公司') != -1 and node_text.find(
                    '（以下简称') != -1 and node_text.find('住所：') != -1):
                item['ent_name'] = self.get_ent_name(node_text)

            # 个人信息特征，男/女、出生，住址：
            elif ((node_text.find('男') != -1 or node_text.find('女') != -1) and node_text.find(
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
        yield item

    def get_ent_name(self, content):
        regex = re.compile(r"当事人：(.*)（以下简称")
        results = regex.findall(content)
        if len(results) > 0:
            return results[0]
        else:
            return None

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

    def get_gender(self,content):
        if content.find('，男，') != -1:
            return '男'
        elif content.find('，女，'):
            return '女'
        else:
            return '未知'