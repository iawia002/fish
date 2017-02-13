#!/usr/bin/env python
# coding=utf-8

import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'

    article_id = sa.Column(
        sa.Integer,
        primary_key=True,
    )
    create_time = sa.Column(
        sa.DateTime,
        default=datetime.datetime.now,
    )
    update_time = sa.Column(
        sa.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )
    title = sa.Column(
        sa.String(100),
    )
    content = sa.Column(
        sa.ARRAY(sa.String),
    )
    image_num = sa.Column(
        sa.Integer,
    )
    source = sa.Column(
        sa.String(1000),
    )

    def __repr__(self):
        return "<Article(id='%d')>" % self.article_id

    @property
    def json(self):
        return {
            'article_id': self.article_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'title': self.title,
            'content': self.content,
            'image_num': self.image_num,
            'source': self.source,
        }


class UpdateInfo(Base):
    __tablename__ = 'update_info'

    update_id = sa.Column(
        sa.Integer,
        primary_key=True,
    )
    content = sa.Column(
        sa.ARRAY(sa.String),
    )
    last_update_time = sa.Column(
        sa.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    def __repr__(self):
        return "<UpdateInfo(last_update_time='%s')>" % (
            self.last_update_time.strftime('%Y-%m-%d %H:%M:%S')
        )
