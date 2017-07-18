# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import datetime
from base import BaseHandler
from tornado.web import authenticated
from operation import merchant
from operation import customer
from operation import consume


class CustomerGbInfoHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '3':
            self.redirect('/index')
        page = self.get_argument('page')
        username = self.get_secure_cookie('username')
        customer_id = self.get_secure_cookie('customer_id')
        db_detail_count = customer.customer_gb_datail_count(customer_id)
        page_num = db_detail_count/10 + 1 if db_detail_count % 10 else db_detail_count/10
        gb_detail_list = customer.get_customer_gb_datail_list(customer_id, int(page))
        info = {
                'page_num': page_num,
                'gb_detail_list': gb_detail_list,
                'page': int(page),
                'username': username
                }
        self.render('customer-goldbean-info.html', **info)


class CustomerGbActivityHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '3':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        customer_id = self.get_secure_cookie('customer_id')
        activity = customer.gb_activity_by_customer_id(customer_id)
        info = {
                'activity': activity,
                'username': username
                }
        self.render('customer-goldbean-activity.html', **info)


class CustomerInfoHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '3':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        customer_id = self.get_secure_cookie('customer_id')
        customer_info = customer.customer_info(customer_id)
        consume_list = consume.consume_get_by_customer_id(customer_id)
        info = {'customer_info': customer_info,
                'username': username,
                'consume_list': consume_list
                }
        self.render('customer-info.html', **info)


class CustomerInfoUpdateHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '3':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        customer_id = self.get_secure_cookie('customer_id')
        customer_info = customer.customer_info(customer_id)
        info = {'customer_info': customer_info,
                'username': username,
                'message': ''
                }
        self.render('customer-info-update.html', **info)

    def post(self):
        username = self.get_secure_cookie('username')
        customer_id = self.get_secure_cookie('customer_id')
        phone = self.get_argument('phone')
        email = self.get_argument('email')
        we_chat = self.get_argument('we_chat')
        info = {'customer_info': {'phone': phone, 'email': email, 'we_chat': we_chat},
                'username': username,
                'message': ''
                }
        message = None
        if not phone:
            message = '手机号码为必填项'
        elif not email:
            message = '邮箱为必填项'
        elif not we_chat:
            message = '微信号为必填项'
        if message:
            info['message'] = message
            self.render('customer-info-update.html', **info)
            return
        try:
            ref = customer.customer_update_by_customer_id(customer_id, phone, email, we_chat)
        except Exception as e:
            info['message'] = e.message
            self.render('customer-info-update.html', **info)
            return
        if ref:
            info['message'] = '修改成功'
            self.render('customer-info-update.html', **info)
