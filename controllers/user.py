# -*- coding: utf-8 -*-
from models.sql.users import Users
from models.sql._base import session
from utils.error import UserNotFind

__author__ = "Sunlf"


class UserController(object):
    @classmethod
    def user_info(cls, user_id):
        pass

    @classmethod
    def user_save(cls):
        user = Users(name="sunlf",
                     password="123456")
        session.add(user)
        session.commit()
