# -*- coding: utf-8 -*-
import os
import tornado.web

__author__ = "Sunlf"


class Router(tornado.web.Application):
    def route(self, url):
        def register(handler):
            view_module = handler.__module__.split(".")[1]      # 提取view module
            view_url = "/{0}{1}".format(view_module, url)       # 拼装新的url
            self.add_handlers(".*$", [(view_url, handler)])
            return handler

        return register


app = Router(debug=bool(int(os.getenv("SERVER_DEBUG"))))

# 加载所有的views,目录中一定要有apis.py文件
view_path = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
for dir_name in os.listdir(view_path):
    dir_path = os.path.join(view_path, dir_name)
    if os.path.isdir(dir_path):
        api_file = os.path.join(dir_path, "apis.py")
        model_path = "{0}.{1}.apis".format(view_path, dir_name)
        if os.path.exists(api_file):
            __import__(model_path)
        else:
            print "View file '{0}' not exists.".format(api_file)
