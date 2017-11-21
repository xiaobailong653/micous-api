# -*- coding: utf-8 -*-
from views._view import BaseView
from views._route import app
from utils.error import UserNotFind
from controllers.user import UserController


__author__ = "Sunlf"


@app.route("/info")
class UserInfo(BaseView):
    def get(self):
        info = UserController.user_info(1)
        self.render(dict(info=info))


@app.route("/create")
class UserCreate(BaseView):
    def post(self):
        UserController.user_save()
        self.render(dict(code=1, message="success"))
