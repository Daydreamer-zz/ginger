#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint
from app.libs.redprint import Redprint
from app.validators.forms import BookSearchForm
from flask import jsonify, request
from app.models.books import Book
# from sqlalchemy import or_
from app.libs.token_auth import auth
from app.validators.forms import PaginateValidator

# blueprint
api = Redprint('book')


@api.route('', methods=['GET'])
@auth.login_required
def get_books():
    params = PaginateValidator().validate_for_api()
    paginator = Book.query.filter_by()\
        .paginate(page=params.page.data, per_page=params.size.data)\
        .hide('summary')
    return jsonify({
        'total': paginator.total,
        'current_page': paginator.page,
        'items': paginator.items
    })


@api.route('/<int:id>', methods=['GET'])
@auth.login_required
def get_book(id=id):
    book = Book.query.filter_by(id=id).first_or_404()
    return jsonify(book)


@api.route('/search', methods=['GET', 'POST'])
@auth.login_required
def search():
    form = BookSearchForm().validate_for_api()
    q = '%' + form.q.data + '%'
    # books = Book.query.filter(
    #     or_(Book.title.like(q), Book.publisher.like(q))
    # ).all()
    books = Book.query.filter(
        (Book.title.like(q) | Book.publisher.like(q))
    ).all()
    books = [book.hide('summary', 'id') for book in books]
    return jsonify(books)
