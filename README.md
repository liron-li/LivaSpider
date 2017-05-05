> 最近学到了python的asyncIO，于是便利用空余时间写了这个小爬虫

##### 环境
- python3.6

##### 依赖：
- beautifulsoup4==4.5.3
- requests==2.13.0
- alembic==0.9.1
- SQLAlchemy==1.1.9

##### 目录结构
```angular2html
├── alembic                  # alembic 目录
│   ├── env.py               # alembic env配置文件
│   ├── README
│   ├── script.py.mako       # alembic 模板文件
│   └── versions             # 表迁移文件
│       └── 404fa70bcf2c_create_tables.py
├── alembic.ini              # alembic 配置文件
├── core
│   ├── crawling.py          # 爬虫基类
│   ├── __init__.py
│   └── models.py            # sqlAlchemy模型
├── example_crawl_baike.py   # example 爬取百度百科
└── README.md
```

##### 如何使用？

- 数据库配置
修改`alembic.ini`文件中的`sqlalchemy.url`
```angular2html
sqlalchemy.url = driver://user:pass@localhost/dbname
```
- 生成表迁移文件
```angular2html
alembic revision --autogenerate -m "your desc"
```

- 执行迁移
```angular2html
alembic upgrade head
```
- 爬虫配置
```angular2html
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
```
爬虫运行时会抓取`start_url`中的符合`url_rule`正则的所有url存入数据库做为爬取的目标url，
直至`url_pool`表中的所有记录都爬取完，爬虫结束


- 运行爬虫
```angular2html
python example_crawl_baike.py
```