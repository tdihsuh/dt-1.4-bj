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
    copname = scrapy.Field()
    org_code = scrapy.Field()
    creditcode = scrapy.Field()
    source_url = scrapy.Field()
    source_page = scrapy.Field()
    spider_name = scrapy.Field()


class TourismItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
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
    compName = scrapy.Field()
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
    companyName = scrapy.Field()
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
    pun_org = scrapy.Field()
    pun_date = scrapy.Field()
    ent_name = scrapy.Field()
    pun_reason = scrapy.Field()
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


class crawler114_out(scrapy.Item):
    case_no = scrapy.Field()
    release_org = scrapy.Field()
    release_date = scrapy.Field()
    ent_name = scrapy.Field()
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
    notice_id = scrapy.Field()



