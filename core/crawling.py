from .models import DBSession, UrlPool
from bs4 import BeautifulSoup
import asyncio
import requests
import urllib
import re


class SpiderBase(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
    }

    cookies = None

    def __init__(self, config):
        self.config = config
        self.db = DBSession()

    def _push_url(self, url):
        """ url存入数据库 """
        res = self.db.query(UrlPool).filter(UrlPool.url == url).one_or_none()
        if res is None:
            new_url = UrlPool(url=url, is_crawl='no')
            self.db.add(new_url)
            self.db.commit()

    def _get_un_crawl_url(self):
        """ 获取一个未爬取的url """
        res = self.db.query(UrlPool).filter(UrlPool.is_crawl == 'no').all()
        if res is not []:
            return res[0].url
        return None

    def get(self, url):
        """ http get """
        response = requests.get(
            url,
            headers=self.config.get('headers', self.headers),
            cookies=self.config.get('cookies', self.cookies)
        )
        return response

    async def async_task(self, url, parse_item):
        """ 异步任务 """
        self._extract_urls(url)
        _loop = asyncio.get_event_loop()
        future = _loop.run_in_executor(None, self.get, url)
        print('crawl: %s' % url)
        response = await future
        parse_item(response)

    def _extract_urls(self, url):
        """ 提取url """
        response = self.get(url)
        url_rule = self.config.get('url_rule')
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            url = urllib.parse.urljoin(self.config.get('base_url'), link.get('href'))
            if re.match(url_rule, url):
                self._push_url(url)

    def _mark_crawled(self, url):
        """ 标记url为已爬取 """
        self.db.query(UrlPool).filter(UrlPool.url == url).update({UrlPool.is_crawl: "yes"})
        self.db.commit()

    def crawl(self, parse_item, start_url=None):
        """ 爬取 """
        url = self.config.get('start_url', start_url)
        if url is None:
            url = self.config.get('start_url')
        # 提取url存入数据库
        self._extract_urls(url)
        start = True
        loop = asyncio.get_event_loop()
        while start:
            url = self._get_un_crawl_url()

            if url is None:
                start = False

            self._mark_crawled(url)
            loop.run_until_complete(self.async_task(url, parse_item))
        loop.close()
