# -*- coding: utf-8 -*-
import tornado.web
from views._route import app

__author__ = "Sunlf"


@app.route("/account/info")
class AccountInfo(tornado.web.RequestHandler):
    def get(self):
        self.finish("ok")
