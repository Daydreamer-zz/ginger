#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import create_app
from app.libs.error import APIException
from werkzeug.exceptions import HTTPException
from app.libs.error_code import ServerError

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    # e可能是
    # APIException
    # HTTPException
    # Exception
    if isinstance(e, APIException):
        return e
    elif isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 可以在这里打日志文件
        # 如果开启调试模式，将显示更详细的错误信息
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run(debug=True)
