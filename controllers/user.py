# -*- coding: utf-8 -*-
from _base import BaseController
from models.sql.users import Users
from models.sql._base import session
from utils.error import UserNotFind

__author__ = "Sunlf"


class UserController(BaseController):
    @classmethod
    def user_info(cls, user_id):
        obj = session.query(Users).get(user_id)
        info = {}
        if obj:
            info = obj.mini_info()
        return info

    @classmethod
    def create_user(cls, info):
        obj = Users(**info)
        user = cls.commit(obj)
        print obj.base_info()
        return obj.base_info()
