# -*- coding: utf-8 -*-
from _base import Base
from sqlalchemy import (
    Column,
    BigInteger,
    TIMESTAMP,
    String,
    text)


class GlobalID(Base):
    __tablename__ = "global_id"
    name = Column(String(32), primary_key=True, nullable=False, index=True)
    value = Column(BigInteger, nullable=False)
    create_time = Column(TIMESTAMP(True), nullable=False, server_default=text('NOW()'))
