#!/usr/bin/env python
# coding=utf-8

# redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 0
REDIS_HOST_PORT = '%(host)s:%(port)s' % {
    'host': REDIS_HOST,
    'port': REDIS_PORT
}

# PSQL
PSQL_HOST = 'localhost'

# sqlalchemy
SA_URL = 'postgresql+psycopg2://:@/fish'

# Article
ARTICLE_PAGE_NUMBER = 10

SECRET_KEY = 'sfljKLYIOY9&()w3rpu39jlfsdf()*))ljsfl&^sfjsfow%*'


try:
    from local_config import *  # noqa
except ImportError:
    pass
