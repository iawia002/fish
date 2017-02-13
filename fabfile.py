#!/usr/bin/env python
# coding=utf-8


from fabric.api import (
    local,
)


def runserver(env='docker'):
    if env == 'local':
        local(
            'python app.py -debug=True'
        )
    else:
        local(
            'DEBUG=True docker-compose run --rm -p 8007:8007 web'
        )


def migrate(env='docker'):
    if env == 'local':
        local(
            'alembic upgrade head'
        )
    else:
        local(
            'docker-compose run --rm web alembic upgrade head'
        )


def shell():
    local(
        'docker-compose run --rm web ipython'
    )


def makemigrations(msg=''):
    local(
        'docker-compose run --rm web alembic revision '
        '--autogenerate -m "{}"'.format(msg)
    )


def init(env='docker'):
    if env == 'local':
        local(
            'python db/init.py'
        )
    else:
        local(
            'docker-compose run --rm web python db/init.py'
        )


def watch():
    local(
        'nodemon -x "python app.py -debug=True" -w static/dist'
    )
