# -*- coding: utf-8 -*-
import os
import hashlib


__author__ = "Sunlf"


class Session(object):
    def make_session_id(cls):
        return hashlib.sha1(os.urandom(24)).hexdigest()
