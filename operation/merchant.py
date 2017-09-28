# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import exception
import user
import datetime
import random
from db import api as db


# 根据user_id查询商户
def get_merchant_by_user_id(user_id):
    return dict(db.merchant_get_by_user_id(user_id))


# 根据id查询商户
def get_merchant_by_id(merchant_id):
    return dict(db.merchant_get_by_id(merchant_id))


# 检查密码
def check_password(merchant_id, password):
    merchant = get_merchant_by_id(merchant_id)
    user_id = merchant['user_id']
    user = db.user_get_by_id(user_id)
    if user['password'] != password:
        raise exception.PasswordIsWrongException()


# 总客户数
def customer_count_by_id(merchant_id):
    return db.customer_count_by_merchant_id(merchant_id)


# 活跃客户数量
def customer_active_count_by_id(merchant_id):
    return db.customer_active_count_by_merchant_id(merchant_id)


# 最近入驻客户户信息
def recent_customer_list(merchant_id):
    temp = db.customer_recent_list_by_merchant_id(merchant_id)
    customer_list = []
    for customer in temp:
        customer_dict = dict(customer)
        customer_list.append(customer_dict)
    return customer_list


# 最近入驻客户数量
def recent_customer_count(merchant_id):
    return db.customer_recent_count_by_merchant_id(merchant_id)


# 最近兑换客户户信息
def recent_exchange_customer_list(merchant_id):
    temp = db.exchange_get_by_merchant_id(merchant_id)
    exchange_list = []
    for exchange in temp:
        exchange_dict = dict(exchange)
        customer = db.customer_get_by_id(exchange_dict['customer_id'])
        exchange_dict['name'] = customer['name']
        exchange_dict['gb'] = customer['gb']
        exchange_list.append(exchange_dict)
    return exchange_list


# 最近兑换客户数量
def recent_exchange_customer_count(merchant_id):
    return db.exchange_recent_count_by_merchant_id(merchant_id)


# 绑定客户
def bind_customer(merchant_id, serial_num, password, name, identify_id, phone, email, we_chat):
    if not db.user_username_if_exist_in_db(serial_num):
        raise exception.UserIsNotExistException()
    user = db.user_get_by_username(serial_num)
    if password != user['password']:
        raise exception.PasswordIsWrongException()
    customer = db.customer_get_by_serial_num(serial_num)
    if customer['merchant_id']:
        raise exception.SerialNumIsAlreadyBinded()
    merchant = db.merchant_get_by_id(merchant_id)
    values = {
        'member_num': merchant['member_num'] + 1
    }
    db.merchant_update_by_id(merchant_id, values)
    values = {
        'merchant_id': merchant_id,
        'name': name,
        'identify_id': identify_id,
        'phone': phone,
        'email': email,
        'we_chat': we_chat
    }
    return db.customer_bind_by_serial_num(serial_num, values)


# 客户列表
def customer_list_by_merchant_id(merchant_id, page):
    customer_count = db.customer_count_by_merchant_id(merchant_id)
    page_num = customer_count/10 + 1 if customer_count % 10 else customer_count/10
    if page < 1 or page > page_num:
        return []
    temp = db.customer_list_by_merchant_id(merchant_id)
    customer_list = []
    count = 1
    for customer in temp:
        customer_dict = dict(customer)
        customer_dict['num'] = count
        customer_list.append(customer_dict)
        count += 1
    return customer_list[10*(page-1):10*page]


# 被查询客户数量
def search_customer_count(merchant_id, type, content):
    if type == '0':
        return db.search_customer_count_by_serial_num(merchant_id, content)
    elif type == '1':
        return db.search_customer_count_by_name(merchant_id, content)
    elif type == '2':
        return db.search_customer_count_by_phone(merchant_id, content)
    elif type == '3':
        min_gb = int(content) * 5000
        max_gb = int(content) * 5000 + 5000 if content != '8'else 1000000000
        return db.search_customer_count_by_gb_range(merchant_id, min_gb, max_gb)


# 被查询客户列表
def get_search_customer_list(merchant_id, page, type, content):
    customer_count = search_customer_count(merchant_id, type, content)
    if type == '0':
        temp = db.customer_list_by_serial_num(merchant_id, content)
    elif type == '1':
        temp = db.customer_list_by_name(merchant_id, content)
    elif type == '2':
        temp = db.customer_list_by_phone(merchant_id, content)
    elif type == '3':
        min_gb = int(content) * 5000
        max_gb = int(content) * 5000 + 5000 if content != '8'else 1000000000
        temp = db.customer_list_by_gb_range(merchant_id, min_gb, max_gb)
    page_num = customer_count/10 + 1 if customer_count % 10 else customer_count/10
    if page < 1 or page > page_num:
        return []
    count = 1
    customer_list = []
    for customer in temp:
        values = dict(customer)
        values['num'] = count
        customer_list.append(values)
        count += 1
    return customer_list[10*(page-1):10*page]


# 商户规则查询
def get_merchant_rule(merchant_id):
    return dict(db.rule_get_by_merchant_id(merchant_id))


# 商户更新兑换规则
def update_merchant_rule(merchant_id, level1, level2, level3, level4, level5, level6, level7, level8, rule_info):
    values = {}
    if level1:
        values['level1'] = level1
    if level2:
        values['level2'] = level2
    if level3:
        values['level3'] = level3
    if level4:
        values['level4'] = level4
    if level5:
        values['level5'] = level5
    if level6:
        values['level6'] = level6
    if level7:
        values['level7'] = level7
    if level8:
        values['level8'] = level8
    if rule_info:
        values['rule_info'] = rule_info
    return db.rule_update_by_merchant_id(merchant_id, values)


# 商户活动查询
def get_merchant_activity(merchant_id):
    return dict(db.activity_get_by_merchant_id(merchant_id))


# 更新活动
def update_merchant_activity(merchant_id, multiple, start_time, end_time):
    values = {
        'multiple': multiple,
        'start_time': start_time,
        'end_time': end_time
    }
    return db.activity_update_by_merchant_id(merchant_id, values)


# 兑换金豆
def exchange_goldbean(merchant_id, serial_num, name, identify_id, ratio):
    customer = db.customer_get_by_serial_num(serial_num)
    if not customer:
        raise exception.SerialNumIsNotExist()
    if name != customer['name'] or identify_id != customer['identify_id']:
        raise exception.CustomerInfoNotMatch()
    if customer['gb'] < int(ratio) * 5000:
        raise exception.CustomerGoldbeanNotEnough()
    if customer['qualification_gb'] < 500:
        raise exception.CustomerHasNoQualification()
    merchant = db.merchant_get_by_id(merchant_id)
    exchange_ratio = get_merchant_rule(merchant_id)
    values = {
        'gb_exchange_count': merchant['gb_exchange_count'] + 1,
        'gb_to_money': merchant['gb_to_money'] + exchange_ratio['level%s' % ratio]
    }
    db.merchant_update_by_id(merchant_id, values)
    values = {
        'gb': customer['gb'] - int(ratio) * 5000,
        'gb_exchange_count': customer['gb_exchange_count'] + 1,
        'gain_money': customer['gain_money'] + exchange_ratio['level%s' % ratio],
        'qualification_gb': 0
    }
    db.customer_update_by_id(customer['id'], values)
    values = {
        'merchant_id': merchant_id,
        'customer_name': customer['name'],
        'customer_id': customer['id'],
        'exchange_money': exchange_ratio['level%s' % ratio],
        'exchange_goldbean': int(ratio) * 5000
    }
    return db.exchange_create(values)


# 金豆兑换排行榜
def exchange_ranking_list(merchant_id):
    temp = db.customer_get_by_merchant_id_order_by_exchange(merchant_id)
    customer_list = []
    for customer in temp:
        customer_dict = dict(customer)
        customer_list.append(customer_dict)
    return customer_list[0:10]


# 总金豆排行榜
def goldbean_ranking_list(merchant_id):
    temp = db.customer_get_by_merchant_id_order_by_goldbean(merchant_id)
    customer_list = []
    for customer in temp:
        customer_dict = dict(customer)
        customer_list.append(customer_dict)
    return customer_list[0:10]


# 兑换数量
def exchange_count_by_id(merchant_id):
    return db.exchange_count_by_merchant_id(merchant_id)


# 兑换列表
def exchange_list_by_merchant_id(merchant_id, page):
    exchange_count = db.exchange_count_by_merchant_id(merchant_id)
    page_num = exchange_count/10 + 1 if exchange_count % 10 else exchange_count/10
    if page < 1 or page > page_num:
        return []
    temp = db.exchange_list_by_merchant_id(merchant_id)
    exchange_list = []
    count = 1
    for exchange in temp:
        exchange_dict = dict(exchange)
        exchange_dict['num'] = count
        exchange_list.append(exchange_dict)
        count += 1
    return exchange_list[10*(page-1):10*page]


# 根据customer_id查找最近兑换记录
def exchange_recent_list_by_customer_id(customer_id):
    temp = db.exchange_get_by_customer_id(customer_id)
    exchange_list = []
    for exchange in temp:
        exchange_list.append(dict(exchange))
    return exchange_list


# 被查询消费数量
def search_exchange_count(merchant_id, type, content):
    if type == '0':
        return db.search_exchange_count_by_customer_name(merchant_id, content)
    elif type == '1':
        min_time = content + ' 00:00:00'
        max_time = content + ' 23:59:59'
        return db.search_exchange_count_by_created_at(merchant_id, min_time, max_time)


# 被查询消费列表
def get_search_exchange_list(merchant_id, page, type, content):
    exchange_count = search_exchange_count(merchant_id, type, content)
    if type == '0':
        temp = db.exchange_list_by_customer_name(merchant_id, content)
    elif type == '1':
        min_time = content + ' 00:00:00'
        max_time = content + ' 23:59:59'
        temp = db.exchange_list_by_created_at(merchant_id, min_time, max_time)
    page_num = exchange_count/10 + 1 if exchange_count % 10 else exchange_count/10
    if page < 1 or page > page_num:
        return []
    count = 1
    exchange_list = []
    for exchange in temp:
        exchange_dict = dict(exchange)
        exchange_dict['num'] = count
        exchange_list.append(exchange_dict)
        count += 1
    return exchange_list[10*(page-1):10*page]


def give_goldbean(customer_id, gb_num):
    customer = db.customer_get_by_id(customer_id)
    values = {
        'merchant_id': customer['merchant_id'],
        'consumer_name': '至尊会员-'.decode('utf-8') + customer['name'],
        'customer_id': customer_id,
        'consume_money': int(gb_num),
        'multiple': 1,
        'consume_content': '商家赠送'
    }
    db.consume_create(values)
    values = {
        'total_gb': customer['total_gb'] + int(gb_num),
        'gb': customer['gb'] + int(gb_num),
        'given_gb': customer['given_gb'] + int(gb_num),
    }
    return db.customer_update_by_id(customer_id, values)



if __name__ == '__main__':
    print customer_active_count_by_id('b8e889de-67ad-11e7-a1d0-3497f688d3c6')