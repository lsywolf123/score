# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user_id")