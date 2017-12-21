# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class ScrapyMigrateProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CustomsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    entity_name = scrapy.Field()
    org_code = scrapy.Field()
    creditcode = scrapy.Field()
    source_url = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()


class TourismItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    entity_name = scrapy.Field()
    legal_person = scrapy.Field()
    permit_number = scrapy.Field()
    penalty_reason = scrapy.Field()
    penalty_content = scrapy.Field()
    penalty_by = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    description = scrapy.Field()
    create_date = scrapy.Field()
    source_url = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()


class crawler005(scrapy.Item):
    punishType = scrapy.Field()
    punishDate = scrapy.Field()
    punishDepartment = scrapy.Field()
    fileNum = scrapy.Field()
    entity_name = scrapy.Field()
    socialUnionNum = scrapy.Field()
    businessRegNum = scrapy.Field()
    fianceNum = scrapy.Field()
    legalMan = scrapy.Field()
    deadLine = scrapy.Field()
    orgNum = scrapy.Field()
    regAddress = scrapy.Field()
    managerRange = scrapy.Field()
    create_date = scrapy.Field()
    source_url = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()


class crawler007(scrapy.Item):
    entity_name = scrapy.Field()
    orgNum = scrapy.Field()
    compAddress = scrapy.Field()
    uncreditContent = scrapy.Field()
    punishResult = scrapy.Field()
    punishBy = scrapy.Field()
    punishDate = scrapy.Field()
    exeDepartment = scrapy.Field()
    create_date = scrapy.Field()
    source_url = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()


class crawler114(scrapy.Item):
    case_no = scrapy.Field()
    punish_agent = scrapy.Field()
    punish_date = scrapy.Field()
    entity_name = scrapy.Field()
    punish_reason = scrapy.Field()
    data_id = scrapy.Field()
    data_source = scrapy.Field()
    del_flag = scrapy.Field()
    op_flag = scrapy.Field()
    create_date = scrapy.Field()
    source_url = scrapy.Field()
    source_page = scrapy.Field()
    reg_no = scrapy.Field()
    report_year = scrapy.Field()
    release_reason = scrapy.Field()
    release_date = scrapy.Field()
    spider_name = scrapy.Field()
    notice_id=scrapy.Field()


class crawler114_out(scrapy.Item):
    case_no = scrapy.Field()
    release_org = scrapy.Field()
    release_date = scrapy.Field()
    entity_name = scrapy.Field()
    release_reason = scrapy.Field()
    data_id = scrapy.Field()
    data_source = scrapy.Field()
    create_date = scrapy.Field()
    source_url = scrapy.Field()
    source_page = scrapy.Field()
    reg_no = scrapy.Field()
    spider_name = scrapy.Field()


class crawler116(scrapy.Item):
    case_no = scrapy.Field()
    punish_type1 = scrapy.Field()
    punish_reason = scrapy.Field()
    law_item = scrapy.Field()
    entity_name = scrapy.Field()
    credit_no = scrapy.Field()
    org_code = scrapy.Field()
    reg_no = scrapy.Field()
    tax_no = scrapy.Field()
    identity_card = scrapy.Field()
    legal_man = scrapy.Field()
    punish_result = scrapy.Field()
    punish_date = scrapy.Field()
    punish_agent = scrapy.Field()
    current_status = scrapy.Field()
    area_code = scrapy.Field()
    offical_updtime = scrapy.Field()
    note = scrapy.Field()
    create_date = scrapy.Field()
    update_date = scrapy.Field()
    punish_type2 = scrapy.Field()
    entity_type = scrapy.Field()
    data_source = scrapy.Field()
    source_url = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()


class C008Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tax_name = scrapy.Field()
    tax_num = scrapy.Field()
    org_num = scrapy.Field()
    reg_address = scrapy.Field()
    legal_man_name = scrapy.Field()
    legal_man_sex = scrapy.Field()
    legal_man_identify_num = scrapy.Field()
    case_nature = scrapy.Field()
    uncredit_content = scrapy.Field()
    create_date = scrapy.Field()
    source_page = scrapy.Field()
    source_url = scrapy.Field()
    spider_name = scrapy.Field()


class C009Item(scrapy.Item):
    credit_icon = scrapy.Field()
    credit_recordNum = scrapy.Field()
    credit_recordBody = scrapy.Field()
    credit_recordBodyDetailUrl = scrapy.Field()
    credit_recordBodyDetailSourceCode = scrapy.Field()
    credit_recordBodyTag = scrapy.Field()
    credit_recordBodyID = scrapy.Field()
    credit_recordBodyGender = scrapy.Field()
    reason = scrapy.Field()
    result = scrapy.Field()
    resultTag = scrapy.Field()
    administration = scrapy.Field()
    notice_id = scrapy.Field()
    recordTime = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()
    source_url = scrapy.Field()


class C010Item(scrapy.Item):
    notice_id = scrapy.Field()  # 系统编码
    filenum = scrapy.Field()
    punishname = scrapy.Field()
    punishtype = scrapy.Field()
    punishreason = scrapy.Field()
    punishaccordance = scrapy.Field()
    personname = scrapy.Field()
    idcard = scrapy.Field()
    punishresult = scrapy.Field()
    timeresult = scrapy.Field()
    punishdepartment = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()


class C012Item(scrapy.Item):
    company_name = scrapy.Field()
    notice_id = scrapy.Field()
    company_detail_pageUrl = scrapy.Field()
    administration = scrapy.Field()
    why_listed_in = scrapy.Field()
    annals_year = scrapy.Field()
    year_listed_in = scrapy.Field()
    create_date = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()



