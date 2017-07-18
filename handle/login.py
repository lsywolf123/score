# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import datetime
from base import BaseHandler
from operation import user
from operation import merchant
from operation import customer


class LoginHandle(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/index')
        else:
            self.render("sign-in.html", message='', username='')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        ref = None
        try:
            ref = user.login(username, password)
        except Exception as e:
            err_msg = e.message
            self.render('sign-in.html', username=username, message=err_msg)
            return
        self.set_secure_cookie('user_id', ref['id'])
        self.set_secure_cookie('role', ref['role'])
        self.set_secure_cookie('username', ref['username'])
        if ref['role'] == '1':
            self.redirect('/index')
        elif ref['role'] == '2':
            merchant_info = merchant.get_merchant_by_user_id(ref['id'])
            if datetime.datetime.now() > merchant_info['deadline']:
                message = '账号已过期，请联系客服'
                self.render('sign-in.html', username=username, message=message)
                return
            self.set_secure_cookie('merchant_id', merchant_info['id'])
            self.redirect('/index')
        elif ref['role'] == '3':
            customer_info = customer.get_customer_by_user_id(ref['id'])
            self.set_secure_cookie('customer_id', customer_info['id'])
            self.redirect('/index')