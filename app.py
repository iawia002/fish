# coding=utf-8

import os

import tornado.web
import tornado.ioloop
from tornado import gen
from tornado.options import (
    define,
    options,
)

import config
import apps.article
import apps.common
from crawler.zhihu import jike


# 在options中设置几个变量
define('port', default=8007, help='run on this port', type=int)
define('debug', default=False, help='enable debug mode')
# options.log_file_prefix = '/etc/logs/zed.tornado.log'


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', apps.article.Index),  # 首页
            (r'/(.*)/', apps.common.Redirect),  # 保证网址有无'/'结尾，都能指向同一个类。
            (r'/p/(\d+)', apps.article.Article),
            (r'/more', apps.article.More),
        ]
        template_path = os.path.join(
            os.path.dirname(__file__), 'static/dist/'
        )
        settings = {
            'static_path': os.path.join(
                os.path.dirname(__file__), 'static'
            ),
            'template_path': template_path,
            'cookie_secret': config.SECRET_KEY,
            'default_handler_class': apps.common.NotFound,
            'login_url': '/login',
            'xsrf_cookies': True,
            'debug': options.debug,
            'gzip': True,
            'autoescape': None
        }
        super(Application, self).__init__(handlers, **settings)

tornado.options.parse_command_line()
application = Application()


@gen.coroutine
def loop():
    while True:
        yield jike()
        yield gen.sleep(60 * 60 * 2)


def main():
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().spawn_callback(loop)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
