# -*- coding: utf-8 -*-

__author__ = "Sunlf"


def Singleton(cls):
    '''实现类的单例模式'''
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
