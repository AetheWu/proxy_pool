#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor, as_completed
import aiohttp
import asyncio

from PIL import Image
from urllib import request,error,parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from proxypool.proxy_log import logger
from proxypool.setting import VALID_STATUS_CODES
'''
利用urllib库从web服务器获取相应
'''

#请求头
REQUESET_HEAD = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}
PROTOCOL = {
    'http':['http://', 'https://']
}

async def get_page(url):
    '''
    获取html页面
    :param url: url地址
    :return: html源码
    '''
    session = aiohttp.ClientSession(headers=REQUESET_HEAD)
    logger.info('开始获取'+url)
    response = await session.get(url)
    if response.status != 200:
        logger.info(url+'获取失败')
        await session.close()
        return None
    logger.info(url+'获取成功')
    html = await response.text()
    print(html)
    await session.close()
    return html

def aio_get_pages(urls):
    tasks = [asyncio.ensure_future(get_page(url)) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    

def get_one_page_by_selenium(url, page_xpath):
    '''
    通过selenium获取html页面，可以爬取动态渲染的网页
    :param url: url地址
    :return: html源码
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    try:
        browser = webdriver.Chrome(chrome_options=chrome_options)
        logger.debug('开始获取'+ url)
        browser.get(url)
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, page_xpath))
        )
        page = browser.page_source
        logger.debug(url+'获取成功')
        return page
    except Exception as e:
        logger.error(url+str(e))
        return None
    finally:
        browser.quit()

def multithread_get_pages(urls, page_xpath):
    pool = ThreadPoolExecutor(len(urls))
    all_tasks = [pool.submit(get_one_page_by_selenium, *(url, page_xpath)) for url in urls]
    for rel in as_completed(all_tasks):
        yield rel.result()



if __name__ =='__main__':
    url = 'http://www.66ip.cn/'
    urls = [url+str(page) for page in range(1,5)]
    page_xpath = '//div[@id="main"]'
    result = multithread_get_pages(urls, page_xpath)
    for i in result:
        print(i)






