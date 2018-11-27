import json
import re
from lxml import etree

from proxypool.get_page import multithread_get_pages
from proxypool.setting import MAX_PAGE,STEP_PAGES
from proxypool.proxy_log import logger

current_page = 1

class MetaClass(type):
    current_page = 1
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

    # def crawl_normal(self):
    #     start_url = 'http://www.89ip.cn/index_'
    #     page_num = 6
    #     pattern = re.compile('\d+')
    #     urls = [start_url+str(page) for page in range(1, page_num+1)]
    #     for url in urls:
    #         page = get_page_by_selenium(url)
    #         if page:
    #             html = etree.HTML(page)
    #             items = html.xpath('//table[@class="layui-table"]/tbody/*')
    #             for item in items:
    #                 ip = '.'.join(re.findall(pattern,item.xpath('./td[1]/text()')[0]))
    #                 port = '.'.join(re.findall(pattern,item.xpath('./td[2]/text()')[0]))
    #                 yield ':'.join([ip,port])

    def crawl_89ip(self, step_pages=STEP_PAGES, max_page=MAX_PAGE):
        '''
        解析代理网站：89ip
        :return: ip地址生成器
        '''
        global current_page
        if current_page + step_pages >= max_page:
            next_page = max_page + 1
        else:
            next_page = current_page + step_pages
        pattern = re.compile('\d+')
        # start_url = 'http://www.89ip.cn/index_'
        start_url = 'http://www.89ip.cn/'
        urls = [start_url + str(page) for page in range(current_page, next_page)]
        if current_page + step_pages >= max_page:
            logger.info('页面爬取数量已达到上限')
            current_page = 1
        else:
            current_page += step_pages
        pages = multithread_get_pages(urls)
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


    # def crawl_66ip(self):
    #     '''
    #     解析代理网站：66ip
    #     :return: ip地址生成器
    #     '''
    #     pattern = re.compile('\d+')
    #     # start_url = 'http://www.89ip.cn/index_'
    #     start_url = 'http://www.66ip.cn/'
    #     page_num = 5
    #     urls = [start_url + str(page) for page in range(1, page_num + 1)]
    #     pages = multithread_get_pages(urls)
    #     for page in pages:
    #         if not page:
    #             break
    #         html = etree.HTML(page)
    #         items = html.xpath('//table[@class="layui-table"]/tbody/*')
    #         if not items:
    #             break
    #         for item in items:
    #             ip = '.'.join(re.findall(pattern, item.xpath('./td[1]/text()')[0]))
    #             port = '.'.join(re.findall(pattern, item.xpath('./td[2]/text()')[0]))
    #             yield ':'.join([ip, port])



if __name__ == '__main__':
    c = Crawler()
    for i in c.crawl_89ip():
        print(i)




