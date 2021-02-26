#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_httpauth import HTTPBasicAuth
from flask import current_app, g, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from app.libs.error_code import AuthFailed, Forbidden
from collections import namedtuple
from app.libs.scope import is_in_scope
from app.models.users import User as Users

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'is_admin'])


@auth.verify_password
def verify_password(token, password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(error_code=1002, msg='token is invalid')
    except SignatureExpired:
        raise AuthFailed(error_code=1003, msg='token is expired')
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)
