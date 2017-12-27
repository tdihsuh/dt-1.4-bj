# -*- coding: utf-8 -*-
# "采集银监会各地银监局的行政处罚信息"
import scrapy
import time
from selenium import webdriver
from scrapy_migrate_project.items import Crawler017Item
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class YjjXingzhengSpider(scrapy.Spider):
    name = 'crawler017_2'
    allowed_domains = ['cbrc.gov.cn']
    start_urls = ['http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current=1']

    def parse(self, response):
        self.flag = 0
        nodes = response.xpath('//div[@class="xia3"]/table[@id="testUI"]//tr')

        # 对于银监局的行政处罚，只有2016年以后的符合抓取格式
        for i in range(0, (len(nodes) - 1), 1):
            item = Crawler017Item()

            td_nodes = nodes[i].xpath(".//td")
            pub_date = nodes[i].xpath(".//td[1]/text()").extract_first().encode('utf-8')

            if pub_date[0:4]=='2015':
                self.flag=-1
                break
            else:
                #提取并下载每个链接
                item['title'] = td_nodes[0].xpath('./a/text()').extract_first().encode('utf-8')
                href = td_nodes[0].xpath('./a/@href').extract_first()
                href = 'http://www.cbrc.gov.cn'+href
                yield scrapy.Request(href,
                                     callback=self.parse_detail,
                                     meta={'item':item})

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

        if current_num < page_num and self.flag == 0:
            i = current_num + 1
            url = 'http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html?current=' + str(i)
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
        if item['title'].find('处罚事项目录') != -1:
            return

        driver = webdriver.PhantomJS(executable_path=sysconfig.get_field('phantomjs', 'path'),
                                    desired_capabilities=dcap);
        driver.get(response.url)
        time.sleep(3)

        main_nodes = driver.find_elements_by_class_name('Section0')
        if (main_nodes==None or len(main_nodes)<1):
            # logger.warn('银监局行政处罚页面结构差异!')
            main_nodes = driver.find_elements_by_class_name('Section1')
            if (main_nodes==None or len(main_nodes)<1):
                main_nodes = driver.find_elements_by_class_name('WordSection1')

        if (main_nodes==None or len(main_nodes) < 1):
            # logger.warn('页面结构异常！处罚文书编号：'+title)
            return
        main_node = main_nodes[0]

        tags = main_node.find_element_by_tag_name('table').find_elements_by_tag_name('tr')
        # 对各个银监局的模板进行处理
        if item['title'].find('吉林银监局') != -1:
            if len(tags) == 10:
                item['case_no'] = tags[0].find_elements_by_tag_name('td')[1].text
                ent_name = tags[3].find_elements_by_tag_name('td')[2].text.encode('utf-8')
                if (ent_name != None and len(ent_name.strip()) >= 6 and ent_name.find('-') == -1):
                    item['entity_name'] = ent_name
                    item['entity_type'] = '2'
                else:
                    item['entity_name'] = tags[1].find_elements_by_tag_name('td')[3].text
                    item['entity_type'] = '1'

                item['case_fact'] = tags[5].find_elements_by_tag_name('td')[1].text
                item['law_item'] = tags[6].find_elements_by_tag_name('td')[1].text
                item['decision'] = tags[7].find_elements_by_tag_name('td')[1].text
                item['pun_org'] = tags[8].find_elements_by_tag_name('td')[1].text
                item['pun_date'] = tags[9].find_elements_by_tag_name('td')[1].text
            else:
                item['case_no'] = tags[0].find_elements_by_tag_name('td')[1].text
                ent_name = tags[2].find_elements_by_tag_name('td')[2].text.encode('utf-8')
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

        elif item['title'].find('江苏银监局') != -1:
            item['case_no'] = tags[0].find_elements_by_tag_name('td')[1].text
            if len(tags) == 7:
                entity_name = tags[1].find_elements_by_tag_name('td')[2].text.encode('utf-8').strip()
                item['entity_name'] = entity_name
                if len(entity_name) >= 6:
                    item['entity_type'] = '2'
                else:
                    item['entity_type'] = '1'

                item['case_fact'] = tags[2].find_elements_by_tag_name('td')[1].text
                item['law_item'] = tags[3].find_elements_by_tag_name('td')[1].text
                item['decision']= tags[4].find_elements_by_tag_name('td')[1].text
                item['pun_org'] = tags[5].find_elements_by_tag_name('td')[1].text
                item['pun_date'] = tags[6].find_elements_by_tag_name('td')[1].text
            else:
                entity_name = tags[1].find_elements_by_tag_name('td')[2].text.encode('utf-8').strip()
                item['entity_name'] = entity_name
                if len(entity_name) >= 6:
                    item['entity_type'] = '2'
                else:
                    item['entity_type'] = '1'
                item['case_fact'] = tags[3].find_elements_by_tag_name('td')[1].text
                item['law_item'] = tags[4].find_elements_by_tag_name('td')[1].text
                item['decision'] = tags[5].find_elements_by_tag_name('td')[1].text
                item['pun_org'] = tags[6].find_elements_by_tag_name('td')[1].text
                item['pun_date'] = tags[7].find_elements_by_tag_name('td')[1].text
        elif item['title'].find('海南银监局') != -1:
            if (len(tags) > 12):
                item['case_no'] = tags[3].find_elements_by_tag_name('td')[1].text
                ent_name = tags[5].find_elements_by_tag_name('td')[2].text.encode('utf-8')
                item['ent_name'] = ent_name
                if (ent_name != None and len(ent_name.strip()) >= 6 and ent_name.find('-') == -1):
                    item['entity_name'] = ent_name
                    item['entity_type'] = '2'
                else:
                    item['entity_name'] = tags[4].find_elements_by_tag_name('td')[2].text
                    item['entity_type'] = '1'
                item['case_fact'] = tags[7].find_elements_by_tag_name('td')[1].text
                item['law_item'] = tags[8].find_elements_by_tag_name('td')[1].text
                item['decision'] = tags[9].find_elements_by_tag_name('td')[1].text
                item['pun_org'] = tags[10].find_elements_by_tag_name('td')[1].text
                item['pun_date'] = tags[11].find_elements_by_tag_name('td')[1].text
            else:
                return
        elif item['title'].find('大连银监局') != -1:
            item['case_no'] = tags[3].find_elements_by_tag_name('td')[1].text
            ent_name = tags[5].find_elements_by_tag_name('td')[2].text.encode('utf-8')
            if (ent_name != None and len(ent_name.strip()) >= 6 and ent_name.find('-') == -1):
                item['entity_name'] = ent_name
                item['entity_type'] = '2'
            else:
                item['entity_name'] = tags[4].find_elements_by_tag_name('td')[2].text
                item['entity_type'] = '1'

            item['case_fact'] = tags[7].find_elements_by_tag_name('td')[1].text
            item['law_item'] = tags[8].find_elements_by_tag_name('td')[1].text
            item['decision'] = tags[9].find_elements_by_tag_name('td')[1].text
            item['pun_org'] = tags[10].find_elements_by_tag_name('td')[1].text
            item['pun_date'] = tags[11].find_elements_by_tag_name('td')[1].text

        else:
            if (len(tags) < 9 or len(tags) > 9):
                # logger.error('页面结构异常！处罚文书：' + title)
                return

            item['case_no'] = tags[0].find_elements_by_tag_name('td')[1].text

            ent_name = tags[2].find_elements_by_tag_name('td')[2].text.encode('utf-8')
            if (ent_name != None and len(ent_name.strip()) >= 4 and ent_name.find('-') == -1 and ent_name.find(
                    '—') == -1):
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

        item['org_level'] = '2'
        item['create_date'] = time.strftime('%Y-%m-%d', time.localtime())
        driver.quit()
        yield item
