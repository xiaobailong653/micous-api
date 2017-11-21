# -*- coding: utf-8 -*-
from datetime import datetime
from _base import Base
from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    TIMESTAMP,
    String,
    text)
from utils.time_tool import TimeHandler as TH


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    gender = Column(SmallInteger())
    email = Column(String(64))
    phone = Column(String(32))
    image = Column(String(128))
    country = Column(String(32))
    city = Column(String(32))
    create_time = Column(TIMESTAMP(True), nullable=False, server_default=text('NOW()'))

    def base_info(self):
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_") and key != "password":
                if isinstance(value, datetime):
                    data[key] = TH.datetime_to_timestamp(value)
                else:
                    data[key] = value
        return data

    def mini_info(self):
        return dict(user_id=self.user_id,
                    name=self.name,
                    gender=self.gender,
                    country=self.country,
                    city=self.city,)
