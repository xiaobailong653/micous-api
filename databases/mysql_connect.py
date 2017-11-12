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


class MysqlHandler(object):
    @classmethod
    def create_engine(cls):
        host_info = "{1}:{2}@{0}:{3}/{4}".format(os.getenv("MYSQL_HOSTNAME"),
                                                 os.getenv("MYSQL_USERNAME"),
                                                 os.getenv("MYSQL_PASSWORD"),
                                                 os.getenv("MYSQL_PORT"),
                                                 os.getenv("MYSQL_DATABASE"))

        return create_engine("mysql+mysqldb://{0}?charset=utf8".format(host_info),
                             pool_recycle=3600)

    @classmethod
    def get_session(cls):

        return sessionmaker(bind=cls.engine)()

    @classmethod
    def mapper_table(cls, t_name):
        table = Table(t_name, self.metadata, autoload=True)

        class Tmp(object):
            pass

        mapper(Tmp, table)

        return table, Tmp


