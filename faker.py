# -*- coding: utf-8 -*-
# !/usr/bin/env python3
from app import create_app
from app.models.users import User
from app.models.base import db


app = create_app()
with app.app_context():
    with db.auto_commit():
        user = User()
        user.nickname = 'admin'
        user.email = 'admin@123.com'
        user.password = '199747'
        db.session.add(user)
