# -*- coding: utf-8 -*-
from datetime import datetime
from models.sql.global_id import GlobalID
from models.sql._base import session
from utils.time_tool import TimeHandler as TH

__author__ = "Sunlf"


class BaseController(object):

    @classmethod
    def create_global_id(cls, model, value=1000000):
        obj = GlobalID(name=model.__tablename__, value=1000000)
        session.add(obj)
        try:
            session.commit()
            return value
        except Exception as ex:
            print "New id commit except, ex={}".format(ex)
            session.rollback()

    @classmethod
    def new_id(cls, model):
        obj = session.query(GlobalID).get(model.__tablename__)
        if obj:
            obj.value += 1
            try:
                session.commit()
            except Exception as ex:
                print "New id commit except, ex={}".format(ex)
                session.rollback()
            return obj.value
        else:
            return cls.create_global_id(model)

    @classmethod
    def commit(cls, objs):
        if isinstance(objs, list):
            for obj in objs:
                session.add(obj)
        elif isinstance(objs, object):
            session.add(objs)
        else:
            print "Argument type error, must list or object."
            return
        try:
            session.commit()
        except Exception as ex:
            print "Commit except, ex={}".format(ex)
            session.rollback()
        return objs

    @classmethod
    def object_to_dict(cls, obj):
        data = {}
        for key, value in obj.__dict__.items():
            if not key.startswith("_"):
                if isinstance(value, datetime):
                    data[key] = TH.datetime_to_timestamp(value)
                else:
                    data[key] = value
        return data
