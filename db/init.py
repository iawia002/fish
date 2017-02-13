#!/usr/bin/env python
# coding=utf-8

from db.sa import Session
from models import UpdateInfo
from crawler.zhihu import jike


def init_update_info():
    session = Session()
    record = UpdateInfo(
        update_id=1,
        content=[],
    )
    session.add(record)
    session.commit()
    session.close()


def init_data():
    jike()


if __name__ == '__main__':
    init_update_info()
    init_data()
