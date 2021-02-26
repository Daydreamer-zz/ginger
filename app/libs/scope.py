# -*- coding: utf-8 -*-
# !/usr/bin/env python3

class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))
        return self


# 普通用户单独配置视图函数权限
# class UserScope(Scope):
#     allow_api = ['v1.user+get_user', 'v1.user+delete_user']

# 普通用户排除管理员视图函数权限
class UserScope(Scope):
    forbidden = ['v1.user+super_get_user', 'v1.user+super_delete_user']

    def __init__(self):
        self + AdminScope()

# Admin权限控制到单个视图函数+普通用户视图函数
# class AdminScope(Scope):
#     allow_api = ['v1.user+super_get_user', 'v1.user+super_delete_user']
#
#     def __init__(self):
#         self + UserScope()


# Admin权限控制到整个视图模块
class AdminScope(Scope):
    allow_module = ['v1.user', 'v1.book', 'v1.gift']


def is_in_scope(scope, endpoint):
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    elif endpoint in scope.allow_api:
        return True
    elif red_name in scope.allow_module:
        return True
    else:
        return False
