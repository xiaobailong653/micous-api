#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import tornado.web
import tornado.ioloop

from views._route import app
from models.sql._base import Base
from databases.mysql_connect import MysqlHandler

__author__ = "Sunlf"

# 设置服务输出日志
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
tornado.log.enable_pretty_logging(logger=logger)

# 加载mysql数据库
mysql_handler = MysqlHandler()
mysql_handler.create_all(Base)

# 启动服务
server_port = os.getenv("SERVER_PORT")
if server_port:
    app.listen(server_port)
    print "The service is listening {0}......".format(server_port)
    tornado.ioloop.IOLoop.instance().start()
else:
    print "The service not set listen port."
