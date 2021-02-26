#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 小程序
    USER_MINA = 200
    # 公众号
    USER_WX = 201