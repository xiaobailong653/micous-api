# -*- coding: utf-8 -*-
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from databases.mysql_connect import MysqlHandler


__author__ = "Sunlf"


Base = declarative_base()

# 加载所有的models
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_name = os.path.basename(dir_path)
for name in os.listdir(dir_path):
    if (not name.startswith("_")) and (not name.endswith("pyc")):
        file_path = os.path.join(dir_path, name)
        if os.path.isfile(file_path):
            model_path = "models.{}.{}".format(dir_name, name.split(".")[0])
            print model_path
            __import__(model_path)

engine = MysqlHandler.create_engine()
Base.metadata.create_all(engine)

SessionCls = sessionmaker(bind=engine)
session = SessionCls()