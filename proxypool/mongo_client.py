from random import choice

import pymongo
from pymongo import errors

from proxypool.setting import MAX_SCORE,MIN_SCORE,INITIAL_SCORE
from proxypool.setting import MONGO_HOST,MONGO_KEY
from proxypool.proxy_log import logger

class MongoClient:
    def __init__(self, host=MONGO_HOST, db_name='test' , collection_name = MONGO_KEY):
        '''
        连接mongo数据库
        :param db_name: 数据库名称
        :param collection_name: 集合名称
        :param host: host地址
        '''
        try:
            self.client = pymongo.MongoClient(host)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            logger.info('连接成功')
        except errors.ConnectionFailure:
            logger.error('连接错误')

    def add(self, proxy:str, score=INITIAL_SCORE):
        '''
        向代理池中添加数据
        :return:
        '''
        try:
            result = self.collection.find_one({'proxy': proxy})
            if not result:
                data = {
                    'proxy': proxy,
                    'score': score
                }
                self.collection.insert_one(data)
                # logger.info('代理添加成功')
            else:
                logger.debug('代理已存在:'+ proxy)
        except errors.OperationFailure:
            logger.error('添加数据错误')
            return None

    def add_many(self, proxies):
        '''
        向代理池中批量添加数据
        :param proxies:
        :return:
        '''
        try:

            if (not proxies) or (not isinstance(proxies, (list, tuple))):
                raise TypeError
            datas = []
            for proxy in set(proxies):
                data = {
                    'proxy':proxy,
                    'score':INITIAL_SCORE
                }
                datas.append(data)
            self.collection.insert_many(datas)
            logger.info('写入成功')
        except TypeError:
            logger.error('传参必须为可迭代')
            return None
        except errors.OperationFailure:
            logger.error('写入失败')
            return None


    def is_exists(self, proxy):
        '''
        判断是否存在该代理地址
        :param proxy:
        :return:
        '''
        return self.collection.find_one({'proxy':proxy})

    def get_proxy(self):
        '''
        优先获取得分最高的代理
        :return:
        '''
        results = self.collection.find({'score':MAX_SCORE})
        if results.count() > 0:
            results = list(results)
            rel = choice(results)
            return rel['proxy']
        else:
            results = self.collection.find({'score':{"$gt":MIN_SCORE,"$lte":MAX_SCORE}}).sort('score',pymongo.DESCENDING)
            if results.count():
                results = list(results)
                rel = choice(results)
                return rel['proxy']
            else:
                logger.warning('代理池空')
                return None

    def set_decrease(self, proxy):
        '''
        代理值分数减一分，分数小于最小值，则代理删除
        :param proxy:
        :return:
        '''
        data = {'proxy':proxy}
        result = self.collection.find_one(data)
        score = result['score']
        if score and score > MIN_SCORE:
            logger.info('代理:%s，当前分数:%d，减1'%(result['proxy'],result['score']) )
            return self.collection.update_one(data, {'$inc':{'score':-1}})
        else:
            logger.info('代理:%s，当前分数:%d，删除'%(result['proxy'],result['score']) )
            return self.collection.delete_one(data)

    def show(self, proxy):
        data = self.collection.find_one({'proxy':proxy})
        print(data)
        # if data:
        #     print(data)
        # else:
        #     print('代理地址不存在')

    def count(self):
        count = self.collection.find().count()
        return count

    def set_max(self, proxy):
        condition = {'proxy':proxy}
        new_data = {'score':MAX_SCORE}
        self.collection.update_one(condition, {'$set': new_data})

    def get_proxier_for_test(self,size):
        '''
        批量获取proxy地址，提供可用性测试
        :param size:测试容量大小
        :return:
        '''
        proxies_iter =  self.collection.find().limit(size)
        return proxies_iter



if __name__ == '__main__':
    m = MongoClient()
    print(m.count())
    result = m.get_proxier_for_test()
    for i in result:
        print(i)


