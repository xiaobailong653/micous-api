# -*- coding: utf-8 -*-
from views._view import BaseView
from views._route import app
from utils.error import UserNotFind

__author__ = "Sunlf"


@app.route("/info")
class UserInfo(BaseView):
    def get(self):

        raise UserNotFind()
