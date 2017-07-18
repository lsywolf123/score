# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
from base import BaseHandler
from tornado.web import authenticated
from operation import manager
from operation import merchant
from operation import customer
from operation import consume


class IndexHandle(BaseHandler):
    @authenticated
    def get(self):
        user_id = self.get_current_user()
        role = self.get_secure_cookie('role')
        username = self.get_secure_cookie('username')
        if user_id:
            if role == '1':
                merchant_count = manager.merchant_count()
                merchant_active_count = merchant_count - manager.merchant_expire_count()
                customer_count = manager.customer_count()
                customer_active_count = manager.customer_active_count()
                merchant_list = manager.recent_merchant_list()
                customer_list = manager.recent_customer_list()
                merchant_recent_count = manager.recent_merchant_count()
                customer_recent_count = manager.recent_customer_count()
                info = {'merchant_count': merchant_count,
                        'merchant_active_count': merchant_active_count,
                        'customer_count': customer_count,
                        'customer_active_count': customer_active_count,
                        'merchant_recent_count': merchant_recent_count,
                        'customer_recent_count': customer_recent_count,
                        'merchant_list': merchant_list,
                        'customer_list': customer_list,
                        'username': username
                        }
                self.render('manager-index.html', **info)
            elif role == '2':
                merchant_id = self.get_secure_cookie('merchant_id')
                merchant_info = merchant.get_merchant_by_id(merchant_id)
                customer_count = merchant.customer_count_by_id(merchant_id)
                customer_active_count = merchant.customer_active_count_by_id(merchant_id)
                customer_recent_list = merchant.recent_customer_list(merchant_id)
                customer_recent_count = merchant.recent_customer_count(merchant_id)
                customer_exchange_recent_list = merchant.recent_exchange_customer_list(merchant_id)
                customer_exchange_recent_count = merchant.recent_exchange_customer_count(merchant_id)
                exchange_ranking_list = merchant.exchange_ranking_list(merchant_id)
                goldbean_ranking_list = merchant.goldbean_ranking_list(merchant_id)
                info = {'customer_count': customer_count,
                        'customer_active_count': customer_active_count,
                        'gb_to_money': merchant_info['gb_to_money'],
                        'gb_exchange_count': merchant_info['gb_exchange_count'],
                        'customer_recent_list': customer_recent_list,
                        'customer_exchange_recent_list': customer_exchange_recent_list,
                        'exchange_ranking_list': exchange_ranking_list,
                        'goldbean_ranking_list': goldbean_ranking_list,
                        'customer_recent_count': customer_recent_count,
                        'customer_exchange_recent_count': customer_exchange_recent_count,
                        'username': username
                        }
                self.render('merchant-index.html', **info)
            elif role == '3':
                customer_id = self.get_secure_cookie('customer_id')
                customer_info = customer.customer_info(customer_id)
                recent_consume_list = consume.recent_consume_list_by_customer_id(customer_id)
                recent_exchange_list = merchant.exchange_recent_list_by_customer_id(customer_id)
                info = {'customer_info': customer_info,
                        'recent_consume_list': recent_consume_list,
                        'recent_exchange_list': recent_exchange_list,
                        'username': username
                        }
                self.render('customer-index.html', **info)
        else:
            self.redirect('/login')