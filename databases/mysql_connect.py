# -*- coding: utf-8 -*-
import os
from sqlalchemy import (
    Column,
    String,
    create_engine,
    MetaData,
    Table)
from sqlalchemy.orm import (
    sessionmaker,
    mapper)
from utils.decorators import Singleton



@Singleton
class MysqlHandler(object):
    def __init__(self):
        self._engine = self.create_engine()

    def create_engine(self):
        host_info = "{1}:{2}@{0}:{3}/{4}".format(os.getenv("MYSQL_HOSTNAME"),
                                                 os.getenv("MYSQL_USERNAME"),
                                                 os.getenv("MYSQL_PASSWORD"),
                                                 os.getenv("MYSQL_PORT"),
                                                 os.getenv("MYSQL_DATABASE"))

        return create_engine("mysql+mysqldb://{0}?charset=utf8".format(host_info),
                             pool_recycle=3600)

    def get_session(self):

        return sessionmaker(bind=self._engine)()

    def create_all(self, base_class):

        base_class.metadata.create_all(self._engine)

    def mapper_table(self, t_name):
        table = Table(t_name, self.metadata, autoload=True)

        class Tmp(object):
            pass

        mapper(Tmp, table)

        return table, Tmp


