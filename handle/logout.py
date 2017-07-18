# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
from base import BaseHandler
from operation import user


class LogoutHandle(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/login')
