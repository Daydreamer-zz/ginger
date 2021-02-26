#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app.libs.redprint import Redprint
from app.validators.forms import ClientForm
from app.libs.enums import ClientTypeEnum
from app.models.users import User
from app.validators.forms import TokenForm
from app.libs.error_code import AuthFailed
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask import current_app, jsonify

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identify = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # 生成Token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(
        identify['uid'],
        form.type.data,
        identify['scope'],
        expiration
    )
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201


@api.route('/secret', methods=['POST'])
def get_token_info():
    form = TokenForm().validate_for_api()
    s = Serializer(secret_key=current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except BadSignature:
        raise AuthFailed(error_code=1002, msg='token is invalid')
    except SignatureExpired:
        raise AuthFailed(error_code=1003, msg='token is expired')
    print(data)
    r = {
        'scope': data[0]['scope'],
        'create_in': data[1]['iat'],
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    return jsonify(r)


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
