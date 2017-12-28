# -*- coding: utf-8 -*-
# "采集银监会各地银监分局的行政处罚信息"
import scrapy
import time
from selenium import webdriver
from scrapy_migrate_project.items import Crawler017Item
# from cycredit.SysConfig import SysConfig as sysconfig
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class YjfjXingzhengSpider(scrapy.Spider):
    name = 'crawler017_3'
    allowed_domains = ['cbrc.gov.cn']
    start_urls = ['http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html?current=1']

    # 列表页
    def parse(self, response):
        nodes = response.xpath('//div[@class="xia3"]/table[@id="testUI"]//tr')
        for i in range(0, (len(nodes) - 1), 1):
            item = Crawler017Item()

            td_nodes = nodes[i].xpath(".//td")
            pub_date = nodes[i].xpath(".//td[1]/text()").extract_first().encode('utf-8')

            # 提取并下载每个链接
            item['title'] = td_nodes[0].xpath('./a/text()').extract_first().encode('utf-8')
            href = td_nodes[0].xpath('./a/@href').extract_first()
            href = 'http://www.cbrc.gov.cn' + href
            yield scrapy.Request(href,
                                 callback=self.parse_detail,
                                 meta={'item': item})

        # 翻页
        url = response.url
        driver2 = webdriver.PhantomJS(executable_path=sysconfig.get_field('phantomjs', 'path'),
                                    desired_capabilities=dcap);
        driver2.get(url)
        time.sleep(3)
        # 获取总页数
        tbody = driver2.find_element_by_id('testUI')
        page_nodes = tbody.find_elements_by_tag_name('tr')
        page_text = page_nodes[len(page_nodes) - 1].text.encode('utf-8')
        page_num = int(page_text[page_text.find('/') + 1:page_text.find('首')].strip())
        current_num = int(page_text[page_text.find(')') + 1:page_text.find('/')].strip())

        driver2.quit()

        if current_num < page_num:
            i = current_num + 1
            url = 'http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html?current='+str(i)
            yield scrapy.Request(url,
                                 callback=self.parse
                                 )

    #详情
    def parse_detail(self, response):
        item = response.meta['item']
        data = response.text
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        item['source_page'] = data
        driver = webdriver.PhantomJS(executable_path=sysconfig.get_field('phantomjs', 'path'),
                                    desired_capabilities=dcap);
        driver.get(response.url)
        time.sleep(3)

        main_nodes = driver.find_elements_by_class_name('Section0')
        if (main_nodes == None or len(main_nodes) < 1):
            # logger.warn('银监局行政处罚页面结构差异!')
            main_nodes = driver.find_elements_by_class_name('Section1')
            if (main_nodes == None or len(main_nodes) < 1):
                main_nodes = driver.find_elements_by_class_name('WordSection1')

        if (main_nodes == None or len(main_nodes) < 1):
            # logger.warn('页面结构异常！处罚文书编号：'+title)
            return
        main_node = main_nodes[0]
        tags = main_node.find_element_by_tag_name('table').find_elements_by_tag_name('tr')
        if (len(tags)<9 or len(tags)>9):
            #logger.warn('页面结构异常！处罚文书：' + title)
            return

        item['case_no'] = tags[0].find_elements_by_tag_name('td')[1].text
        ent_name = tags[2].find_elements_by_tag_name('td')[2].text
        if (ent_name != None and len(ent_name.strip()) >= 6 and ent_name.find('-') == -1):
            item['entity_name'] = ent_name
            item['entity_type'] = '2'
        else:
            item['entity_name'] = tags[1].find_elements_by_tag_name('td')[2].text
            item['entity_type'] = '1'

        item['case_fact'] = tags[4].find_elements_by_tag_name('td')[1].text
        item['law_item'] = tags[5].find_elements_by_tag_name('td')[1].text
        item['decision'] = tags[6].find_elements_by_tag_name('td')[1].text
        item['pun_org'] = tags[7].find_elements_by_tag_name('td')[1].text
        item['pun_date'] = tags[8].find_elements_by_tag_name('td')[1].text
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        item['org_level'] = '3'

        driver.quit()
        yield item