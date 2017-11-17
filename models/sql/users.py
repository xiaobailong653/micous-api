# -*- coding: utf-8 -*-
from _base import Base
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    SmallInteger,
    TIMESTAMP,
    String,
    text)


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
