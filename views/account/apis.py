# -*- coding: utf-8 -*-
import json
from views._view import BaseView
from views._route import app
from controllers.user import UserController

__author__ = "Sunlf"


@app.route("/user/register")
class AccountInfo(BaseView):
    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("password")
        args = {}
        if name and password:
            args["name"] = name
            args["password"] = password
            args["gender"] = int(self.get_argument("gender", 1))
            args["email"] = self.get_argument("email", "")
            args["phone"] = self.get_argument("phone", "")
            args["image"] = self.get_argument("image", "")
            args["country"] = self.get_argument("country", "CN")
            args["city"] = self.get_argument("city", "")
            info = UserController.create_user(args)
        self.render(dict(info=info))
