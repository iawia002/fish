#!/usr/bin/env python
# coding=utf-8

import utils.db
import utils.common

from db.sa import Session

from models import (
    Article as ArticleModel,
)

from apps.base import BaseHandler


class Index(BaseHandler):
    def get(self):
        data = {}
        articles = utils.db.article(page=1)
        data['articles'] = articles
        data['next_page'] = 2
        self.render('index.html', data=data)


class More(BaseHandler):
    def get(self):
        next_page = self.get_argument('next_page')
        articles = utils.db.article(page=next_page)

        if not articles:
            return self.write('')
        data = {}
        data['articles'] = articles
        article_list = self.render_string('article_list.html', data=data)
        ret = {
            'next_page': int(next_page) + 1,
            'data': article_list
        }
        self.write(ret)


class Article(BaseHandler):
    def get(self, article_id):
        session = Session()
        article = session.query(ArticleModel).filter(
            ArticleModel.article_id == article_id,
        ).first()
        if not article:
            return utils.common.raise_error(request=self, status_code=404)
        article = article.json
        session.commit()
        session.close()
        data = {}
        data['article'] = article
        self.render('article.html', data=data)