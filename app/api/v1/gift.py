# -*- coding: utf-8 -*-
# !/usr/bin/env python3
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.gift import Gift
from app.models.books import Book
from app.libs.error_code import DuplicateGift, Success
from flask import g

api = Redprint('gift')


@api.route('/<isbn>', methods=['POST'])
@auth.login_required
def create(isbn):
    uid = g.user.uid
    with db.auto_commit():
        Book.query.filter_by(isbn=isbn).first_or_404()
        gift = Gift.query.filter_by(isbn=isbn, uid=uid).first()
        if gift:
            raise DuplicateGift()
        gift = Gift()
        gift.isbn = isbn
        gift.uid = uid
        db.session.add(gift)
    return Success()
