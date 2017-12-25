# -*- coding: utf-8 -*-
# "采集银监会行政处罚信息"
import scrapy
import time
from selenium import webdriver
from scrapy_migrate_project.items import Crawler017Item



class YjhXingzhengSpider(scrapy.Spider):
    name = 'crawler017'
    allowed_domains = ['cbrc.gov.cn']
    start_urls = ['http://www.cbrc.gov.cn/chinese/home/docViewPage/110002&current=1']

    # 列表页
    def parse(self, response):
        nodes = response.xpath('//div[@class="xia3"]/table[@id="testUI"]//a')

        # 提取每个链接的详细信息，逐条下载
        for node in nodes:
            item = Crawler017Item()
            title = node.xpath('./text()').extract_first().encode('utf-8')
            href = node.xpath('./@href').extract_first()
            href = 'http://www.cbrc.gov.cn'+href
            if title.find('中国银监会行政处罚信息公开表') != -1:
                item['title'] = title
                yield scrapy.Request(href,
                                     callback=self.parse_detail,
                                     meta={'item':item}
                                     )
        # 翻页
        url = response.url
        driver2 = webdriver.Chrome('C:\Python27\selenium\webdriver\chromedriver_win32\chromedriver.exe')
        driver2.get(url)
        time.sleep(3)
            # 获取总页数
        tbody = driver2.find_element_by_id('testUI')
        page_nodes = tbody.find_elements_by_tag_name('tr')
        page_text = page_nodes[len(page_nodes) - 1].text.encode('utf-8')
        page_num = int(page_text[page_text.find('/') + 1:page_text.find('首')].strip())
        current_num =  int(page_text[page_text.find(')') + 1:page_text.find('/')].strip())

        driver2.quit()

        if current_num < page_num:
            i = current_num + 1
            url ='http://www.cbrc.gov.cn/chinese/home/docViewPage/110002&current='+str(i)
            yield scrapy.Request(url,
                                callback=self.parse
                                )


    #详情页
    def parse_detail(self, response):
        item = response.meta['item']
        data = response.text
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        item['source_page'] = data
        driver = webdriver.Chrome('C:\Python27\selenium\webdriver\chromedriver_win32\chromedriver.exe')
        driver.get(response.url)
        time.sleep(3)

        main_nodes = driver.find_elements_by_class_name('Section0')
        if (main_nodes == None or len(main_nodes) < 1):
            main_nodes = driver.find_elements_by_class_name('Section1')
        main_node = main_nodes[0]

        tags = main_node.find_element_by_tag_name('table').find_elements_by_tag_name('tr')

        item['case_no'] = tags[0].find_elements_by_tag_name('td')[1].text

        person_name = tags[1].find_elements_by_tag_name('td')[2].text
        if (person_name!=None and len(person_name.strip())>0):
            item['entity_name'] = person_name
            item['entity_type'] = '1'
        else:
            item['entity_name'] = tags[2].find_elements_by_tag_name('td')[2].text
            item['entity_type'] = '2'

        item['case_fact'] = tags[4].find_elements_by_tag_name('td')[1].text
        item['law_item'] = tags[5].find_elements_by_tag_name('td')[1].text
        item['decision'] = tags[6].find_elements_by_tag_name('td')[1].text
        item['pun_org'] = tags[7].find_elements_by_tag_name('td')[1].text
        item['pun_date'] = tags[8].find_elements_by_tag_name('td')[1].text

        item['org_level'] = '1'
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        driver.quit()
        yield item
