import json
import re
from lxml import etree

from proxypool.get_page import multithread_get_pages
from proxypool.setting import MAX_PAGE,STEP_PAGES
from proxypool.proxy_log import logger

current_page89 = 1
current_page66 = 1

class MetaClass(type):

    def __new__(cls, name, bases, attrs):
        '''
        为Crawler类增加两个属性：crawl函数名称和函数个数
        :param name:
        :param bases:
        :param attrs:
        :return:
        '''
        count = 0
        attrs['__crawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__crawlFunc__'].append(k)
                count += 1
        attrs['__crawlCount__'] = count
        return super().__new__(cls, name, bases, attrs)


class Crawler(metaclass=MetaClass):

    def get_proxy(self,func):
        proxy_list = list(eval('self.%s()' %(func)))
        return proxy_list

    def crawl_66ip(self, step_pages=STEP_PAGES, max_page=MAX_PAGE):
        '''
        解析代理网站：66ip
        :return: 
        '''
        global current_page66
        page_xpath = '//div[@id="main"]'

        if current_page66 + step_pages >= max_page:
            next_page = max_page + 1
        else:
            next_page = current_page66 + step_pages
        
        start_url = 'http://www.66ip.cn/'
        urls = [start_url + str(page) for page in range(current_page66, next_page)]
        if current_page66 + step_pages >= max_page:
            logger.info('页面爬取数量已达到上限')
            current_page66 = 1
        else:
            current_page66 += step_pages
        pages = multithread_get_pages(urls, page_xpath)
        for page in pages:
            if not page:
                break
            html = etree.HTML(page)
            items = html.xpath('//div[@id="main"]//table/tbody/tr[1]/following-sibling::*')
            if not items:
                break
            for item in items:
                ip = item.xpath('./td[1]/text()')[0]
                port = item.xpath('./td[2]/text()')[0]
                yield ':'.join([ip, port])
        

    def crawl_89ip(self, step_pages=STEP_PAGES, max_page=MAX_PAGE):
        '''
        解析代理网站：89ip
        :return: ip地址生成器
        '''
        global current_page89
        page_xpath = '//table[@class="layui-table"]'

        if current_page89 + step_pages >= max_page:
            next_page = max_page + 1
        else:
            next_page = current_page89 + step_pages
        pattern = re.compile('\d+')
        start_url = 'http://www.89ip.cn/'
        urls = [start_url + str(page) for page in range(current_page89, next_page)]
        if current_page89 + step_pages >= max_page:
            logger.info('页面爬取数量已达到上限')
            current_page89 = 1
        else:
            current_page89 += step_pages
        pages = multithread_get_pages(urls, page_xpath)
        for page in pages:
            if not page:
                break
            html = etree.HTML(page)
            items = html.xpath('//table[@class="layui-table"]/tbody/*')
            if not items:
                break
            for item in items:
                ip = '.'.join(re.findall(pattern, item.xpath('./td[1]/text()')[0]))
                port = '.'.join(re.findall(pattern, item.xpath('./td[2]/text()')[0]))
                yield ':'.join([ip, port])

if __name__ == '__main__':
    c = Crawler()
    for i in c.crawl_66ip():
        print(i)




