#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Redprint(object):
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        return decorator

    def register(self, bp, url_prefix=None):
        """
        :param bp: Flask的原生蓝图对象
        :param url_prefix: 视图包的路由
        """
        if url_prefix is None:
            # 默认使用实例化Redprint的模块名作为url_prefix，省去再去定义url_prefix
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = self.name + "+" + options.pop('endpoint', f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)