# -*- coding: utf-8 -*-
import time
from datetime import datetime


class TimeHandler(object):
    @classmethod
    def time(cls):
        return int(time.time())

    @classmethod
    def time13(cls):
        return int(time.time() * 1000)

    @classmethod
    def OneHour(cls):
        return 60 * 60

    @classmethod
    def OneHour13(cls):
        return cls.OneHour() * 1000

    @classmethod
    def OneDay13(cls):
        return cls.OneHour13() * 24

    @classmethod
    def OneDay(cls):
        return cls.OneHour() * 24

    @classmethod
    def OneWeek(cls):
        return 7 * cls.OneDay()

    @classmethod
    def OneWeek13(cls):
        return 1000 * cls.OneWeek()

    @classmethod
    def timestamp_to_time(cls, timestamp, zone=0):
        timestamp += zone * cls.OneHour()
        timeArray = time.localtime(timestamp)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    @classmethod
    def timestamp_to_date(cls, timestamp, zone=0):
        timestamp += zone * cls.OneHour()
        timeArray = time.localtime(timestamp)
        return time.strftime("%Y-%m-%d", timeArray)

    @classmethod
    def time_to_timestamp13(cls, str_time):
        return int(time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S')) * 1000)

    @classmethod
    def time_to_timestamp(cls, str_time):
        return int(time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S')))

    @classmethod
    def datetime_to_timestamp(cls, date_time):
        return int(time.mktime(date_time.timetuple()))
