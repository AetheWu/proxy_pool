import aiohttp
import asyncio
import time
import sys
from aiohttp import ClientError,ClientProxyConnectionError,ServerTimeoutError,ClientTimeout
from concurrent.futures._base import TimeoutError

from proxypool.mongo_client import MongoClient
from proxypool.proxy_log import logger
from proxypool.setting import TEST_URL,VALID_STATUS_CODES,BATCH_TEST_SIZE

class TestProxy:
    def __init__(self):
        self.mongo = MongoClient()

    async def test_proxy(self, proxy):
        '''
        检测代理地址可用性
        :param proxy:str类型的代理地址
        :return:None
        '''
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                real_proxy = 'http://' + proxy
                logger.debug(proxy+'开始测试')
                async with session.get(TEST_URL, proxy=real_proxy, timeout=10) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.mongo.set_max(proxy)
                        logger.debug(proxy+'代理可用')
                    else:
                        self.mongo.set_decrease(proxy)
                        logger.debug(proxy+'响应码不合法')
            except Exception as e:
                self.mongo.set_decrease(proxy)
                logger.info(proxy+str(e))
            # except (ServerTimeoutError,ClientTimeout):
            #     self.mongo.set_decrease(proxy)
            #     logger.info(proxy+'代理连接超时')
            # except ClientError:
            #     self.mongo.set_decrease(proxy)
            #     logger.info(proxy+'客户端连接错误')
            # except ClientProxyConnectionError:
            #     logger.info(proxy+'代理连接无法建立')
            # except asyncio.TimeoutError:
            #     logger.info(proxy+'协程等待超时')
            # except Exception:
            #     logger.error(proxy+'其他错误')

    def run(self,size=BATCH_TEST_SIZE):
        try:
            count = self.mongo.count()
            logger.info('当前代理数量:%d'%count)
            if not count:
                logger.info('代理池为空')
                return None
            test_proxies = self.mongo.get_proxier_for_test(size)
            # self.test_proxy(proxy)['proxy']
            loop = asyncio.get_event_loop()
            tasks = [self.test_proxy(proxy['proxy']) for proxy in test_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception:
            logger.error('测试器发生错误')

if __name__ == '__main__':
    tester = TestProxy()
    tester.run()
