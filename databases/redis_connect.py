# -*- coding: utf-8 -*-
import os
import redis


class RedisHandler(object):

    @classmethod
    def redis_cli(cls):
        config = dict(host=os.getenv("REDIS_HOST"),
                      port=os.getenv("REDIS_PORT"),
                      db=os.getenv("REDIS_DB"))
        return redis.StrictRedis(**config)
