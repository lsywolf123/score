# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import datetime
from base import BaseHandler
from operation import user
from tornado.web import authenticated


class UpdatePasswordHandle(BaseHandler):
    @authenticated
    def get(self):
        username = self.get_secure_cookie('username')
        self.render('update-password.html', username=username, message='')

    def post(self):
        user_id = self.get_secure_cookie('user_id')
        username = self.get_secure_cookie('username')
        old_password = self.get_argument('old_password')
        new_password1 = self.get_argument('new_password1')
        new_password2 = self.get_argument('new_password2')
        message = None
        if not old_password:
            message = '旧密码为必填项'
        elif not new_password1:
            message = '新密码为必填项'
        elif not new_password2:
            message = '请确认新密码'
        elif new_password1 != new_password2:
            message = '两次密码不一致'
        if message:
            self.render('update-password.html', username=username, message=message)
            return
        try:
            user.check_password(user_id, old_password)
            ref = user.update_password(user_id, new_password1)
        except Exception as e:
            self.render('update-password.html', username=username, message=e.message)
            return
        if ref:
            self.render('update-password.html', username=username, message='修改成功')