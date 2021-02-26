#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:199747@127.0.0.1/ginger'
# SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'ginger.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'kexl88PdATh72Yee'