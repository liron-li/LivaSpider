"""
    sqlAlchemy模型
    生成迁移文件：alembic revision --autogenerate -m "desc"
    执行迁移：alembic upgrade head
"""
from sqlalchemy import create_engine, Column, Integer, String, Enum, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class UrlPool(Model):
    """ url地址池表模型 """
    __tablename__ = "url_pool"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    url = Column(String(500))
    is_crawl = Column(Enum('yes', 'no'), default='no', nullable=False)


class Baike(Model):
    """ 百度百科表模型 """
    __tablename__ = "baike"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(100))
    description = Column(String(2000))


# 初始化数据库连接:
engine = create_engine('mysql://root:123456@192.168.33.110:3306/spider?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
