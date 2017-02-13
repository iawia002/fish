#!/usr/bin/env python
# coding=utf-8

from db.sa import Session
from models import UpdateInfo


def init_update_info():
    session = Session()
    record = UpdateInfo(
        update_id=1,
        content=[],
    )
    session.add(record)
    session.commit()
    session.close()


if __name__ == '__main__':
    init_update_info()
