# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pykafka import KafkaClient
from scrapy.exceptions import DropItem

from scrapy_migrate_project.items import TourismItem

import redis

from scrapy_migrate_project.items import crawler114

redis_db = redis.Redis(host='10.3.10.33', port=6379, db=0, password=None)
redis_data_dict = "scrapy_test"

class ScrapyMigrateProjectPipeline(object):

    def __init__(self,producer):

        self.producer1 = producer[0]
        self.producer2 = producer[1]

    @classmethod
    def from_settings(cls,settings):
        list_class = []
        host = settings['KAFKA_HOST']
        client = KafkaClient(host)
        topic = client.topics['test1']
        topic2 = client.topics['test']
        producer = topic.get_producer()
        producer2 = topic2.get_producer()

        list_class.append(producer)
        list_class.append(producer2)

        return cls(list_class)



    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.producer1.produce(bytes(content))

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

        return item

