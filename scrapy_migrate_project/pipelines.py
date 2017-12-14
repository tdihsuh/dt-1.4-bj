# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pykafka import KafkaClient

from scrapy.exceptions import DropItem

from scrapy_migrate_project import settings
from scrapy_migrate_project.items import TourismItem, crawler116, CustomsItem, crawler007, crawler114_out

import redis

from scrapy_migrate_project.items import crawler114

redis_db = redis.Redis(host='10.3.10.33', port=6379, db=0, password=None)
redis_data_dict = "scrapy_test"

class ScrapyMigrateProjectPipeline(object):

    def __init__(self,producer):
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



    @classmethod
    def from_settings(cls,settings):
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

        return cls(list_class)



    def process_item(self, item, spider):

        if isinstance(item, crawler114):
            # self.producer_oe.produce(str(dict(item)))
            content = json.dumps(dict(item), ensure_ascii=False)
            self.producer_oe.produce(str(content))
        elif isinstance(item, CustomsItem):
            content = json.dumps(dict(item), ensure_ascii=False)
            self.producer_cu.produce(str(content))
        elif isinstance(item, TourismItem):
            content = json.dumps(dict(item), ensure_ascii=False)
            self.producer_tr.produce(str(content))
        elif isinstance(item, crawler116):
            self.producer_ap.produce(str(item))
        elif isinstance(item, crawler007):
            content = json.dumps(dict(item), ensure_ascii=False)
            self.producer_gp.produce(str(content))
        elif isinstance(item, crawler114_out):
            self.producer_oe.produce(str(dict(item)))


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
                redis_db.hset(redis_data_dict, item['source_url'], 1)
        elif item['spider_name'] == 'c116a11':
            if redis_db.hexists(redis_data_dict, item['noticeid']):
                print('already exist!')
                raise DropItem("Duplicate item found:%s" % item)
            else:
                redis_db.hset(redis_data_dict, item['noticeid'], item['spider_name'])

        return item

