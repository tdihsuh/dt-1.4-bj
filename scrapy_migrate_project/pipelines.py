# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pykafka import KafkaClient

from scrapy.exceptions import DropItem

from scrapy_migrate_project.items import TourismItem, crawler116, CustomsItem, crawler007, crawler114_out, crawler005

import redis

from scrapy_migrate_project.items import crawler114
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

redis_db = redis.Redis(host='10.3.10.33', port=6379, db=0, password=None)
redis_data_dict = "scrapy_test"


class ScrapyMigrateProjectPipeline(object):

    def __init__(self, producer):
        # def __init__(self):

        # self.file_tourism = open('tourism.json', 'wb')
        # self.file_customs = open('customs.json', 'wb')
        # self.file_C116a11Item = open('C116a11Item.json', 'wb')
        # self.file_crawler114_1 = open('crawler114_1.json', 'wb')
        # self.file_crawler114_3_out = open('crawler114_3_out.json', 'wb')
        # self.file_crawler114_5 = open('crawler114_5.json', 'wb')
        # self.file_crawler114_5_out = open('crawler114_5_out.json', 'wb')
        # self.file_crawler114_6 = open('crawler114_6.json', 'wb')
        # self.file_crawler114_6_out = open('crawler114_6_out.json', 'wb')
        # self.file_crawler114_7 = open('crawler114_7.json', 'wb')
        # self.file_crawler114_7_out = open('crawler114_7_out.json', 'wb')
        # self.file_crawler114_8 = open('crawler114_8.json', 'wb')
        # self.file_crawler114_8_out = open('crawler114_8_out.json', 'wb')
        # self.file_crawler116_1 = open('crawler116_1.json', 'wb')
        # self.file_crawler116_4 = open('crawler116_4.json', 'wb')
        # self.file_crawler116_6 = open('crawler116_6.json', 'wb')
        self.producer_cm = producer[0]
        self.producer_oe = producer[1]
        self.producer_gp = producer[2]
        self.producer_sp = producer[3]
        self.producer_fm = producer[4]
        self.producer_ta = producer[5]
        self.producer_dp = producer[6]
        self.producer_cb = producer[7]
        self.producer_qb = producer[8]
        self.producer_ap = producer[9]
        self.producer_ag = producer[10]
        self.producer_mt = producer[11]
        self.producer_cu = producer[12]
        self.producer_tr = producer[13]
        self.producer_cs = producer[14]
        self.producer_sb = producer[15]
        self.producer_ci = producer[16]
        self.producer_cd = producer[17]

    @classmethod
    def from_settings(cls, settings):
        list_class = []
        host = settings['KAFKA_HOST']
        client = KafkaClient(host)
        topic_cm = client.topics['tag_cm']
        topic_oe = client.topics['tag_oe']
        topic_gp = client.topics['tag_gp']
        topic_sp = client.topics['tag_sp']
        topic_fm = client.topics['tag_fm']
        topic_ta = client.topics['tag_ta']
        topic_dp = client.topics['tag_dp']
        topic_cb = client.topics['tag_cb']
        topic_qb = client.topics['tag_qb']
        topic_ap = client.topics['tag_ap']
        topic_ag = client.topics['tag_ag']
        topic_mt = client.topics['tag_mt']
        topic_cu = client.topics['tag_cu']
        topic_tr = client.topics['tag_tr']
        topic_cs = client.topics['tag_cs']
        topic_sb = client.topics['tag_sb']
        topic_ci = client.topics['tag_ci']
        topic_cd = client.topics['tag_cd']
        producer_cm = topic_cm.get_producer()
        producer_oe = topic_oe.get_producer()
        producer_gp = topic_gp.get_producer()
        producer_sp = topic_sp.get_producer()
        producer_fm = topic_fm.get_producer()
        producer_ta = topic_ta.get_producer()
        producer_dp = topic_dp.get_producer()
        producer_cb = topic_cb.get_producer()
        producer_qb = topic_qb.get_producer()
        producer_ap = topic_ap.get_producer()
        producer_ag = topic_ag.get_producer()
        producer_mt = topic_mt.get_producer()
        producer_cu = topic_cu.get_producer()
        producer_tr = topic_tr.get_producer()
        producer_cs = topic_cs.get_producer()
        producer_sb = topic_sb.get_producer()
        producer_ci = topic_ci.get_producer()
        producer_cd = topic_cd.get_producer()

        list_class.append(producer_cm)
        list_class.append(producer_oe)
        list_class.append(producer_gp)
        list_class.append(producer_sp)
        list_class.append(producer_fm)
        list_class.append(producer_ta)
        list_class.append(producer_dp)
        list_class.append(producer_cb)
        list_class.append(producer_qb)
        list_class.append(producer_ap)
        list_class.append(producer_ag)
        list_class.append(producer_mt)
        list_class.append(producer_cu)
        list_class.append(producer_tr)
        list_class.append(producer_cs)
        list_class.append(producer_sb)
        list_class.append(producer_ci)
        list_class.append(producer_cd)

        return cls(list_class)

    def process_item(self, item, spider):
        if isinstance(item, crawler114):
            print(item['ent_name'])
            self.producer_oe.produce(str(item))

        elif isinstance(item, CustomsItem):
            print(item['entity_name'])
            content = json.dumps(dict(item), ensure_ascii=False)
            self.producer_cu.produce(str(content))
        elif isinstance(item, TourismItem):
            print(item['entity_name'])
            content = json.dumps(dict(item), ensure_ascii=False)
            self.producer_tr.produce(str(content))
        elif isinstance(item, crawler116):
            print(item['entity_name'])
            self.producer_ap.produce(str(item))
        elif isinstance(item, crawler007):
            print(item['entity_name'])
            content = json.dumps(dict(item), ensure_ascii=False)
            self.producer_gp.produce(str(content))
        elif isinstance(item, crawler114_out):

            print(item['ent_name'])
            self.producer_oe.produce(str(item))
            # self.producer_oe.produce(str(item))
        elif isinstance(item, crawler005):
            print(item['entity_name'])
            self.producer_cd.produce(str(item))

        return item

    def close_spider(self, spider):
        pass


class DuplicatePipeline(object):

    def process_item(self, item, spider):
        if item['spider_name'] == 'crawler114_7':
            if redis_db.hexists(redis_data_dict, item['source_url']):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, item['source_url'], item['spider_name'])
        elif item['spider_name'] == 'crawler114_7_out':
            if redis_db.hexists(redis_data_dict, item['source_url']):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, item['source_url'], item['spider_name'])
        elif item['spider_name'] == 'crawler114_8':
            if redis_db.hexists(redis_data_dict, hash(item['case_no'] + item['pun_date'] + item['ent_name'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['case_no'] + item['pun_date'] + item['ent_name']),
                              item['spider_name'])
        elif item['spider_name'] == 'crawler114_8_out':
            if redis_db.hexists(redis_data_dict, hash(item['case_no'] + item['release_date'] + item['ent_name'])):
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['case_no'] + item['release_date'] + item['ent_name']),
                              item['spider_name'])

        elif item['spider_name'] == 'crawler114_6':
            if redis_db.hexists(redis_data_dict, hash(item['case_no'] + item['pun_date'] + item['ent_name'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['case_no'] + item['pun_date'] + item['ent_name']),
                              item['spider_name'])

        elif item['spider_name'] == 'crawler114_6_out':
            if redis_db.hexists(redis_data_dict, hash(item['case_no'] + item['release_date'] + item['ent_name'])):
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['case_no'] + item['release_date'] + item['ent_name']),
                              item['spider_name'])

        elif item['spider_name'] == 'crawler114_5':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'crawler114_5_out':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'crawler114_1':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'crawler114_3':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'crawler114_3_out':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'crawler116_6':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'crawler116_1':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'crawler116_4':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'customs_spider':
            if redis_db.hexists(redis_data_dict, hash(item['org_code'] + item['copname'] + item['creditcode'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['org_code'] + item['copname'] + item['creditcode']),
                              item['spider_name'])

        elif item['spider_name'] == 'tourism_spider':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        elif item['spider_name'] == 'crawler007':
            if redis_db.hexists(redis_data_dict, hash(item['entity_name']+item['punishDate']+item['orgNum'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict,hash(item['entity_name']+item['punishDate']+item['orgNum']), item['spider_name'])

        elif item['spider_name'] == 'crawler005':
            if redis_db.hexists(redis_data_dict, hash(item['source_url'])):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, hash(item['source_url']), item['spider_name'])

        return item
