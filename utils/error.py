# -*- coding: utf-8 -*-

__author__ = "Sunlf"


class DictError(Exception):
    def dump(self):
        return {"code": self.code, "message": self.message}

    def __str__(self):
        return "error_code=%s,%s" % (self.code, self.message)


class MethodNotFind(DictError):
    code = 405
    message = "Method not find."


class UserNotFind(DictError):
    code = 1001
    message = "User not find."
