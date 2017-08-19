# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import time
from base import BaseHandler
from tornado.web import authenticated
from operation import manager
from operation import user
from operation import customer
from operation import consume


def now():
    return time.strftime("%Y-%m-%d", time.localtime())


class MerchantListHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        page = self.get_argument('page')
        username = self.get_secure_cookie('username')
        type = self.get_argument('type')
        content = self.get_argument('content')
        if type and content:
            merchant_count = manager.search_merchant_count(type, content)
            page_num = merchant_count / 10 + 1 if merchant_count % 10 else merchant_count / 10
            merchant_list = manager.get_search_merchant_list(1, type, content)
        else:
            merchant_count = manager.merchant_count()
            page_num = merchant_count/10 + 1 if merchant_count % 10 else merchant_count/10
            merchant_list = manager.get_merchant_list(int(page))
        info = {'page_num': page_num,
                'merchant_list': merchant_list,
                'page': int(page),
                'username': username,
                'type': type,
                'content': content,
                }
        self.render('manager-users.html', **info)

    def post(self):
        type = self.get_argument('type')
        username = self.get_secure_cookie('username')
        content = self.get_argument('content')
        search_merchant_count = manager.search_merchant_count(type, content)
        page_num = search_merchant_count / 10 + 1 if search_merchant_count % 10 else search_merchant_count / 10
        search_merchant_list = manager.get_search_merchant_list(1, type, content)
        info = {'page_num': page_num,
                'merchant_list': search_merchant_list,
                'page': 1,
                'username': username,
                'type': type,
                'content': content
                }
        self.render('manager-users.html', **info)


class AddMerchantHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        self.render('manager-add-user.html', username=username, message='', name='', host_name='', phone='',
                    email='', address='', deadline=now())

    def post(self):
        message = None
        username = self.get_secure_cookie('username')
        name = self.get_argument('name')
        host_name = self.get_argument('host_name')
        phone = self.get_argument('phone')
        email = self.get_argument('email')
        address = self.get_argument('address')
        deadline = self.get_argument('deadline')
        if not name:
            message = '商家名称为必填项'
        elif not host_name:
            message = '店主名字为必填项'
        elif not phone:
            message = '手机号码为必填项'
        elif not email:
            message = '邮箱为必填项'
        elif not address:
            message = '地址为必填项'
        if message:
            self.render('manager-add-user.html', message=message, name=name, host_name=host_name, phone=phone,
                        email=email, address=address, deadline=deadline)
            return
        try:
            ref = manager.add_merchant(name, host_name, phone, email, address, deadline)
        except Exception as e:
            err_msg = e.message
            self.render('manager-add-user.html', username=username, message=err_msg, name=name, host_name=host_name,
                        phone=phone, email=email, address=address, deadline=deadline)
            return
        if ref:
            self.render('manager-add-user.html', username=username, message='添加成功',  name='', host_name='',
                        phone='', email='', address='', deadline=now())


class UpdateMerchantHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        merchant_id = self.get_argument('id')
        merchant = manager.merchant_get_by_id(merchant_id)
        self.render('manager-update-user.html', username=username, message='', id=merchant_id, name=merchant['name'],
                    host_name=merchant['host_name'],phone=merchant['phone'], email=merchant['email'],
                    address=merchant['address'],deadline=merchant['deadline'])

    def post(self):
        username = self.get_secure_cookie('username')
        name = self.get_argument('name')
        host_name = self.get_argument('host_name')
        phone = self.get_argument('phone')
        email = self.get_argument('email')
        address = self.get_argument('address')
        deadline = self.get_argument('deadline')
        merchant_id = self.get_argument('id')
        try:
            ref = manager.update_merchant(merchant_id, name, host_name, phone, email, address, deadline)
        except Exception as e:
            err_msg = e.message
            self.render('manager-update-user.html', username=username, message=err_msg, id=merchant_id, name=name,
                        host_name=host_name, phone=phone,email=email, address=address, deadline=deadline)
            return
        if ref:
            self.render('manager-update-user.html', username=username, message='修改成功', id=merchant_id, name=ref['name'],
                        host_name=ref['host_name'],phone=ref['phone'], email=ref['email'], address=ref['address'],
                        deadline=ref['deadline'])


class DeleteMerchantHandle(BaseHandler):
    @authenticated
    def post(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        merchant_id = self.get_argument('id')
        ref = manager.merchant_delete_by_id(merchant_id)
        if ref:
            self.redirect('/merchant-list?page=1')


class AddCustomerHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        self.render('manager-add-customer.html', username=username, start_num='', end_num='', message='')

    def post(self):
        message = None
        username = self.get_secure_cookie('username')
        start_num = self.get_argument('start_num')
        end_num = self.get_argument('end_num')
        password = self.get_argument('password')
        user_ref = user.get_user_by_username(username)
        if password != user_ref['password']:
            message = '密码错误'
        if not start_num:
            message = '起始编号为必填项'
        if not end_num:
            message = '结束编号为必填项'
        try:
            if int(start_num) < 0:
                message = '起始编号必须为大于0的数字'
            if int(end_num) < 0:
                message = '结束编号必须为大于0的数字'
            if int(start_num) > int(end_num):
                message = '结束编号必须不小于起始编号'
        except:
            message = '编号必须是数字'
        if not password:
            message = '密码为必填项'
        if message:
            self.render('manager-add-customer.html', username=username, start_num='', end_num='', message=message)
            return
        try:
            ref = manager.add_customer(int(start_num), int(end_num))
        except Exception as e:
            self.render('manager-add-customer.html', username=username, start_num='', end_num='', message=e.message)
            return
        if ref:
            self.render('manager-add-customer.html', username=username, start_num='', end_num='', message='添加成功')
            return


class CustomerAddedListHandle(BaseHandler):
    def get(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        page = self.get_argument('page')
        result = manager.get_added_customer_list(int(page))
        added_customer_list = result[0]
        page_num = result[1]
        info = {'page_num': page_num,
                'added_customer_list': added_customer_list,
                'page': int(page),
                'username': username
                }
        self.render('manager-add-customer-list.html', **info)


class CustomerAddedInfoHandle(BaseHandler):
    def get(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        page = self.get_argument('page')
        created_time = self.get_argument('created_time')
        added_customer_info_list = manager.get_added_customer_info(created_time, int(page))
        added_customer_info_count = manager.get_add_customer_info_count(created_time)
        page_num = added_customer_info_count / 10 + 1 if added_customer_info_count % 10 else added_customer_info_count / 10
        info = {'page_num': page_num,
                'added_customer_info_list': added_customer_info_list,
                'page': int(page),
                'username': username,
                'created_time': created_time
                }
        self.render('manager-add-customer-info.html', **info)


class CustomerListHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        type = self.get_argument('type')
        content = self.get_argument('content')
        page = self.get_argument('page')
        username = self.get_secure_cookie('username')
        if type and content:
            customer_count = manager.search_customer_count(type, content)
            page_num = customer_count / 10 + 1 if customer_count % 10 else customer_count / 10
            customer_list = manager.get_search_customer_list(int(page), type, content)
        else:
            customer_count = manager.customer_count()
            page_num = customer_count/10 + 1 if customer_count % 10 else customer_count/10
            customer_list = manager.customer_list(int(page))
        info = {'type': type,
                'content': content,
                'page_num': page_num,
                'customer_list': customer_list,
                'page': int(page),
                'username': username
                }
        self.render('manager-customers.html', **info)

    def post(self):
        type = self.get_argument('type')
        username = self.get_secure_cookie('username')
        content = self.get_argument('content%s'%type)
        customer_count = manager.search_customer_count(type, content)
        page_num = customer_count / 10 + 1 if customer_count % 10 else customer_count / 10
        customer_list = manager.get_search_customer_list(1, type, content)
        info = {'type': type,
                'content': content,
                'page_num': page_num,
                'customer_list': customer_list,
                'page': 1,
                'username': username
                }
        self.render('manager-customers.html', **info)


class ManagerCustomerInfoHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '1':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        customer_id = self.get_argument('customer_id')
        customer_info = customer.customer_info(customer_id)
        consume_list = consume.consume_all_list_by_customer_id(customer_id)
        info = {'customer_info': customer_info,
                'username': username,
                'consume_list': consume_list
                }
        self.render('manager-customer-info.html', **info)
