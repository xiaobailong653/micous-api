# -*- coding: utf-8 -*-
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

__author__ = "Sunlf"


Base = declarative_base()
host_info = "{1}:{2}@{0}:{3}/{4}".format(os.getenv("MYSQL_HOSTNAME"),
                                         os.getenv("MYSQL_USERNAME"),
                                         os.getenv("MYSQL_PASSWORD"),
                                         os.getenv("MYSQL_PORT"),
                                         os.getenv("MYSQL_DATABASE"))

engine = create_engine("mysql+mysqldb://{0}?charset=utf8".format(host_info),
                       pool_recycle=3600)
session = sessionmaker(bind=engine)()
