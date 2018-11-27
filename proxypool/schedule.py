"调度模块，多进程启动三个模块"

import time

from concurrent.futures import ProcessPoolExecutor

from proxypool.proxy_log import logger
from proxypool.api import app
from proxypool.get_proxy import GetProxy
from proxypool.test_proxy import TestProxy
from proxypool.setting import TEST_CYCLE,GET_CYCLE,API_ENABLED,GET_ENABLED,TEST_ENABLED

class Scheduler():
    def schedule_get(self, cycle=GET_CYCLE):
        '''
        定时抓取代理地址
        :param cycle:循环周期
        :return:
        '''
        getter = GetProxy()
        while True:
            logger.info('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_test(self, cycle=TEST_CYCLE):
        '''
        定时测试代理地址
        :param cycle:
        :return:
        '''
        tester = TestProxy()
        while True:
            logger.info('开始测试代理')
            tester.run()
            time.sleep(cycle)

    def schedule_api(self):
        '''
        开启api网页
        :return:
        '''
        app.run()

    def run(self):
        logger.info('代理池开始运行')
        pool = ProcessPoolExecutor(3)
        if GET_ENABLED:
            pool.submit(fn=self.schedule_get)

        if TEST_ENABLED:
            pool.submit(fn=self.schedule_test)

        if API_ENABLED:
            pool.submit(fn=self.schedule_api)




