# -*- coding: utf-8 -*-
# 爬取信用辽宁黑名单数据
import scrapy
from bs4 import BeautifulSoup
from scrapy_migrate_project.items import Crawler013Item
import uuid
import time


class LnHeimingdanSpider(scrapy.Spider):
    name = 'crawler013'
    allowed_domains = ['218.60.146.14']
    start_urls = ['http://218.60.146.14:8082/xyln_badList/fenye.html?pageNum=1']

    # 列表页
    def parse(self, response):
        url = response.url
        cur_page = int(url.split("=")[-1])
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        atag = soup.find_all('a')
        for i in range(len(atag)):
            item = Crawler013Item()
            i = i + 3
            try:
                link = atag[i]['href']
            except:
                continue
            name = atag[i].get_text(strip=True)
            item['base_company_name'] = name
            if link.find('http://218.60.146.14:8082/xyln_badList/xxy.htm?xybsm=') != -1:
                yield scrapy.Request(link,
                                     callback=self.parse_detail,
                                     meta={'item':item})
        # 拿到总页数
        p = soup.find_all(class_='f12 f_black_one lh20 ml20 fl')
        strp = p[0].get_text(strip=True)
        listp = strp.split(unicode('，', 'utf8'))
        items = listp[0].encode('utf-8')
        totalitems = filter(str.isalnum, items)
        totalitems = int(totalitems)
        if totalitems % 25 == 0:
            totalpages = totalitems / 25
        else:
            totalpages = totalitems // 25 + 1
        # 翻页
        if cur_page < totalpages:
            cur_page += 1
            href = 'http://218.60.146.14:8082/xyln_badList/fenye.html?pageNum='+str(cur_page)
            yield scrapy.Request(href,
                                 callback=self.parse)

    # 详情页
    def parse_detail(self, response):
        item = response.meta['item']
        url = response.url
        item['source_url'] = url
        item['spider_name'] = self.name
        data = response.text
        item['source_page'] = data
        soup2 = BeautifulSoup(data, "lxml")
        foreign_id = uuid.uuid1()
        foreign_id_str = str(foreign_id)
        create_date = time.strftime('%Y-%m-%d', time.localtime())
        tabletag = soup2.find_all('table')
        for jjj in range(len(tabletag)):
            jjj = jjj + 1
            if jjj == len(tabletag):
                continue
            detail = tabletag[jjj].get_text(strip=True)
            if detail:
                tdtag = tabletag[jjj].find_all('td')
                m = 0
                list = []
                dic = {}
                for every2 in tdtag:
                    subsubdetail = every2.get_text(strip=True)
                    if ':' in subsubdetail:
                        subsubdetail = subsubdetail.replace(':', '')
                    list.append(subsubdetail)
                    m = m + 1
                    if m == 2:
                        dic[list[0]] = list[1]
                        list = []
                        m = 0

                if dic.has_key(unicode('企业名称', 'utf8')):
                    compname = dic[unicode('企业名称', 'utf8')].replace(' ', '')
                    item['comp_name'] = compname

                if dic.has_key(unicode('处罚事项', 'utf8')):
                    punishreason3 = dic[unicode('处罚事项', 'utf8')].replace(' ', '')
                    item['punish_reason3'] = punishreason3

                if dic.has_key(unicode('相关法律依据及税务处理处罚情况', 'utf8')):
                    lawandtaxresult = dic[unicode('相关法律依据及税务处理处罚情况', 'utf8')].replace(' ', '')
                    item['law_and_tax_result'] = lawandtaxresult

                if dic.has_key(unicode('组织机构代码', 'utf8')):
                    orgnum = dic[unicode('组织机构代码', 'utf8')].replace(' ', '')
                    item['org_num'] =  orgnum

                if dic.has_key(unicode('纳税人识别号', 'utf8')):
                    taxpersonnum = dic[unicode('纳税人识别号', 'utf8')].replace(' ', '')
                    item['tax_person_num'] = taxpersonnum

                if dic.has_key(unicode('录入时间', 'utf8')):
                    inputtime = dic[unicode('录入时间', 'utf8')].replace(' ', '')
                    item['input_time'] = inputtime

                if dic.has_key(unicode('法定代表人', 'utf8')):
                    legalman = dic[unicode('法定代表人', 'utf8')].replace(' ', '')
                    item['legal_man'] = legalman

                if dic.has_key(unicode('案件性质', 'utf8')):
                    casenature = dic[unicode('案件性质', 'utf8')].replace(' ', '')
                    item['case_nature'] = casenature

                if dic.has_key(unicode('注册地址', 'utf8')):
                    regaddress = dic[unicode('注册地址', 'utf8')].replace(' ', '')
                    item['reg_address'] = regaddress

                if dic.has_key(unicode('录入单位', 'utf8')):
                    inputunit = dic[unicode('录入单位', 'utf8')].replace(' ', '')
                    item['input_unit'] = inputunit

                if dic.has_key(unicode('主要违法事实', 'utf8')):
                    illegalfact = dic[unicode('主要违法事实', 'utf8')].replace(' ', '')
                    item['illegal_fact'] = illegalfact

                if dic.has_key(unicode('处罚日期', 'utf8')):
                    punishdate = dic[unicode('处罚日期', 'utf8')].replace(' ', '')
                    item['punish_date'] = punishdate

                if dic.has_key(unicode('处罚机构', 'utf8')):
                    punishagent = dic[unicode('处罚机构', 'utf8')].replace(' ', '')
                    item['punish_agent'] = punishagent

                if dic.has_key(unicode('处罚金额（万元）', 'utf8')):
                    punishsum = dic[unicode('处罚金额（万元）', 'utf8')].replace(' ', '')
                    item['punish_sum'] = punishsum

                if dic.has_key(unicode('处罚依据', 'utf8')):
                    punishby = dic[unicode('处罚依据', 'utf8')].replace(' ', '')
                    item['punish_by'] = punishby

                if dic.has_key(unicode('处罚结果', 'utf8')):
                    punishresult = dic[unicode('处罚结果', 'utf8')].replace(' ', '')
                    item['punish_result'] = punishresult

                if dic.has_key(unicode('处罚内容', 'utf8')):
                    punishcontent = dic[unicode('处罚内容', 'utf8')].replace(' ', '')
                    item['punish_content'] = punishcontent

                if dic.has_key(unicode('立案编号', 'utf8')):
                    casenum = dic[unicode('立案编号', 'utf8')].replace(' ', '')
                    item['case_num'] = casenum

                if dic.has_key(unicode('处罚种类', 'utf8')):
                    punishtype = dic[unicode('处罚种类', 'utf8')].replace(' ', '')
                    item['punish_type'] = punishtype

                if dic.has_key(unicode('处理结果', 'utf8')):
                    exeresult = dic[unicode('处理结果', 'utf8')].replace(' ', '')
                    item['exe_result'] = exeresult

                if dic.has_key(unicode('处罚原因', 'utf8')):
                    punishreason = dic[unicode('处罚原因', 'utf8')].replace(' ', '')
                    item['punish_reason'] = punishreason

                if dic.has_key(unicode('地方编码', 'utf8')):
                    areacode = dic[unicode('地方编码', 'utf8')].replace(' ', '')
                    item['area_code'] = areacode

                if dic.has_key(unicode('工商登记码', 'utf8')):
                    bussinessnum = dic[unicode('工商登记码', 'utf8')].replace(' ', '')
                    item['bussiness_num'] = bussinessnum

                if dic.has_key(unicode('处罚类别2', 'utf8')):
                    punishtype2 = dic[unicode('处罚类别2', 'utf8')].replace(' ', '')
                    item['punish_type2'] = punishtype2

                if dic.has_key(unicode('统一社会信用代码', 'utf8')):
                    socialunioncreditnum = dic[unicode('统一社会信用代码', 'utf8')].replace(' ', '')
                    item['social_union_credit_num'] = socialunioncreditnum

                if dic.has_key(unicode('处罚类别1', 'utf8')):
                    punishtype1 = dic[unicode('处罚类别1', 'utf8')].replace(' ', '')
                    item['punish_type1'] = punishtype1

                if dic.has_key(unicode('税务登记号', 'utf8')):
                    taxnum = dic[unicode('税务登记号', 'utf8')].replace(' ', '')
                    item['tax_num'] = taxnum

                if dic.has_key(unicode('行政相对人名称', 'utf8')):
                    administrationman = dic[unicode('行政相对人名称', 'utf8')].replace(' ', '')
                    item['administration_man'] = administrationman

                if dic.has_key(unicode('处罚名称', 'utf8')):
                    punishname = dic[unicode('处罚名称', 'utf8')].replace(' ', '')
                    item['punish_name'] = punishname

                if dic.has_key(unicode('法定代表人姓名', 'utf8')):
                    legalman2 = dic[unicode('法定代表人姓名', 'utf8')].replace(' ', '')
                    item['legal_man2'] = legalman2

                if dic.has_key(unicode('行政处罚决定书文号', 'utf8')):
                    punishfilenum = dic[unicode('行政处罚决定书文号', 'utf8')].replace(' ', '')
                    item['punish_file_num'] = punishfilenum

                if dic.has_key(unicode('处罚决定日期', 'utf8')):
                    punishdate2 = dic[unicode('处罚决定日期', 'utf8')].replace(' ', '')
                    item['punish_date2'] = punishdate2

                if dic.has_key(unicode('居民身份证号', 'utf8')):
                    identifynum = dic[unicode('居民身份证号', 'utf8')].replace(' ', '')
                    item['identify_num'] = identifynum

                if dic.has_key(unicode('处罚状态', 'utf8')):
                    punishstatus = dic[unicode('处罚状态', 'utf8')].replace(' ', '')
                    item['punish_status'] = punishstatus

                if dic.has_key(unicode('处罚行政机构', 'utf8')):
                    punishagent2 = dic[unicode('处罚行政机构', 'utf8')].replace(' ', '')
                    item['punish_agent2'] = punishagent2

                if dic.has_key(unicode('处罚事由', 'utf8')):
                    punishreason2 = dic[unicode('处罚事由', 'utf8')].replace(' ', '')
                    item['punish_reason2'] = punishreason2

                if dic.has_key(unicode('备注', 'utf8')):
                    note = dic[unicode('备注', 'utf8')].replace(' ', '')
                    item['note'] = note

                if dic.has_key(unicode('时间戳', 'utf8')):
                    timestamp = dic[unicode('时间戳', 'utf8')].replace(' ', '')
                    item['timestamp'] = timestamp

                if dic.has_key(unicode('发布时间', 'utf8')):
                    reporttime = dic[unicode('发布时间', 'utf8')].replace(' ', '')
                    item['report_time'] = reporttime

                if dic.has_key(unicode('注册地', 'utf8')):
                    regaddress2 = dic[unicode('注册地', 'utf8')].replace(' ', '')
                    item['reg_address2'] = regaddress2

                if dic.has_key(unicode('信息自采来源', 'utf8')):
                    infosource = dic[unicode('信息自采来源', 'utf8')].replace(' ', '')
                    item['info_source'] = infosource

                if dic.has_key(unicode('被列入黑名单原因', 'utf8')):
                    blacklistreason = dic[unicode('被列入黑名单原因', 'utf8')].replace(' ', '')
                    item['blacklist_reason'] = blacklistreason

                if dic.has_key(unicode('企业法人姓名', 'utf8')):
                    legalman3 = dic[unicode('企业法人姓名', 'utf8')].replace(' ', '')
                    item['legal_man3'] = legalman3

                if dic.has_key(unicode('案号', 'utf8')):
                    casenum1 = dic[unicode('案号', 'utf8')].replace(' ', '')
                    item['case_num1'] = casenum1

                if dic.has_key(unicode('作出执行依据单位', 'utf8')):
                    exeagent = dic[unicode('作出执行依据单位', 'utf8')].replace(' ', '')
                    item['exe_agent'] = exeagent

                if dic.has_key(unicode('地域ID', 'utf8')):
                    areacode1 = dic[unicode('地域ID', 'utf8')].replace(' ', '')
                    item['area_code1'] = areacode1

                if dic.has_key(unicode('失信被执行人具体情形', 'utf8')):
                    uncreditsituation = dic[unicode('失信被执行人具体情形', 'utf8')].replace(' ', '')
                    item['uncredit_situation'] = uncreditsituation

                if dic.has_key(unicode('法律生效文书确定的义务', 'utf8')):
                    obligation = dic[unicode('法律生效文书确定的义务', 'utf8')].replace(' ', '')
                    item['obligation'] = obligation

                if dic.has_key(unicode('执行法院', 'utf8')):
                    execourt = dic[unicode('执行法院', 'utf8')].replace(' ', '')
                    item['exe_court'] = execourt

                if dic.has_key(unicode('地域名称', 'utf8')):
                    areaname = dic[unicode('地域名称', 'utf8')].replace(' ', '')
                    item['area_name'] = areaname

                if dic.has_key(unicode('正式处罚文号', 'utf8')):
                    punishfilenum2 = dic[unicode('正式处罚文号', 'utf8')].replace(' ', '')
                    item['punish_file_num2'] = punishfilenum2

                if dic.has_key(unicode('正式处罚下达日期', 'utf8')):
                    punishdate3 = dic[unicode('正式处罚下达日期', 'utf8')].replace(' ', '')
                    item['punish_date3'] = punishdate3

                if dic.has_key(unicode('违法事由', 'utf8')):
                    punishreason4 = dic[unicode('违法事由', 'utf8')].replace(' ', '')
                    item['punish_reason4'] = punishreason4

                if dic.has_key(unicode('罚款金额', 'utf8')):
                    punishsum2 = dic[unicode('罚款金额', 'utf8')].replace(' ', '')
                    item['punish_sum2'] = punishsum2
                    create_date = time.strftime('%Y-%m-%d', time.localtime())
                item['create_date'] = create_date

        yield item