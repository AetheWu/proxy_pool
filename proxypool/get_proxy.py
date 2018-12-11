from proxypool.crawl import Crawler
from proxypool.mongo_client import MongoClient
from proxypool.proxy_log import logger
from proxypool.setting import POOL_CAPACITY

class GetProxy:
    def __init__(self, crawler, mongo):
        self.crawler = crawler
        self.mongo = mongo

    def run(self):
        if self.mongo.count() >= POOL_CAPACITY:
            logger.info('代理池地址数量已达容量上限')
            return None
        for i in range(self.crawler.__crawlCount__):
            func = self.crawler.__crawlFunc__[i]
            logger.info('获取代理地址数据集')
            proxies = self.crawler.get_proxy(func)
            logger.info('数据数量:'+str(len(proxies)))
            logger.info('开始写入数据库...')
            self.mongo.add_many(proxies)

if __name__ == '__main__':
    get = GetProxy()
    get.run()