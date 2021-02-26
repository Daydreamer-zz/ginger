#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.error_code import ServerError
from datetime import datetime, date


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        # 将sqlalchemy对象返回为字典格式
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder

