from core import models, crawling
from bs4 import BeautifulSoup


class Spider(crawling.SpiderBase):
    @staticmethod
    def parse_item(response):
        soup = BeautifulSoup(response.text, 'html.parser')
        db = models.DBSession()

        if soup.h1 is not None and soup.find('div', class_="lemma-summary") is not None:
            title = soup.h1.text.strip()
            description = soup.find('div', class_="lemma-summary").text.strip()

            db.execute('SET NAMES utf8;')
            db.execute('SET CHARACTER SET utf8;')
            db.execute('SET character_set_connection=utf8;')
            print('title : %s' % title)
            print("description : %s" % description)
            new_row = models.Baike(
                title=title.encode(response.encoding),
                description=description.encode(response.encoding)
            )
            db.add(new_row)
            db.commit()


if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
    }
    cookies = {

    }
    config = {
        # 请求头
        "headers": headers,
        # cookies
        "cookies": cookies,
        # 根url
        "base_url": "http://baike.baidu.com/",
        # 起始url
        "start_url": "http://baike.baidu.com/item/%E9%93%81%E6%A0%91/110475",
        # 抓取的网站正则
        "url_rule": r'^http://baike.baidu.com/item/',
    }
    spider = Spider(config)
    spider.crawl(Spider.parse_item)
