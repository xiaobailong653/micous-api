# -*- coding: utf-8 -*-
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from databases.mysql_connect import MysqlHandler


__author__ = "Sunlf"


Base = declarative_base()
session = MysqlHandler().get_session()
