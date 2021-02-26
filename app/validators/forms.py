#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, NumberRange
from wtforms import ValidationError
from app.validators.base import BaseForm
from app.libs.enums import ClientTypeEnum
from app.models.users import User


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(min=5,max=35)])
    secret = StringField(validators=[DataRequired()])
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='不是邮箱格式')])
    secret = StringField(validators=[
        DataRequired(),
        # Regexp(r'^[A-Za-z0-9_*&$#@]{6, 22}$', message='密码必须包含大小写和特殊字符')
    ])
    nickname = StringField(validators=[DataRequired(message='昵称不能为空'), length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError(message=f'已经存在用户名为{value.data}的用户')


class BookSearchForm(BaseForm):
    q = StringField(validators=[DataRequired()])


class TokenForm(BaseForm):
    token = StringField(validators=[DataRequired()])


class PaginateValidator(BaseForm):
    page = IntegerField('当前页数', validators=[NumberRange(min=1)], default=1)
    size = IntegerField('每页条数', validators=[NumberRange(min=1, max=10)], default=10)

    def validate_page(self, value):
        self.page.data = int(value.data)

    def validate_size(self, value):
        self.size.data = int(value.data)
