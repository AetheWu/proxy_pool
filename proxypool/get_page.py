#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image
from urllib import request,error,parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from proxypool.proxy_log import logger
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

def get_page(url):
    '''
    获取html页面
    :param url: url地址
    :return: html源码
    '''
    try:
        rel = parse.urlparse(url)
    except error.URLError:
        retval = 'url数据类型错误'
        return retval
    if not rel.scheme:
        url = PROTOCOL['http'][0] + url
    req = request.Request(url, headers=REQUESET_HEAD)
    try:
        f = request.urlopen(req)
        if f.status == 200:
            return f.read()
    except error.URLError:
        retval = '无效url'
        return retval

def get_one_page_by_selenium(url):
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
            EC.presence_of_all_elements_located((By.XPATH, '//*'))
        )
        page = browser.page_source
        logger.debug(url+'获取成功')
        # f = browser.get_screenshot_as_file('page.png')
        # f = Image.open('page.png')
        # f.show()
        return page
    except Exception as e:
        logger.error(url+str(e))
        return None
    finally:
        browser.quit()

def multithread_get_pages(urls):
    pool = ThreadPoolExecutor(len(urls))
    all_results = pool.map(get_one_page_by_selenium, urls)
    return all_results

if __name__ =='__main__':
    url = 'http://www.66ip.cn/'
    urls = [url + str(page) for page in range(1,5)]
    multithread_get_pages(urls)






