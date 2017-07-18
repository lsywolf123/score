# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import exception
import user
import datetime
import random
from db import api as db


# 生成消费信息
def general_consume_info(merchant_id, consumer_name, consume_money, consume_content, serial_num):
    values = {
        'merchant_id': merchant_id,
        'consumer_name': consumer_name,
        'consume_money': consume_money,
        'multiple': 1.0
    }
    if consume_content:
        values['consume_content'] = consume_content
    if serial_num:
        recomender = db.customer_get_by_serial_num(serial_num)
        if not recomender:
            raise exception.SerialNumIsNotExist()
        values['customer_id'] = recomender['id']
        activity = db.activity_get_by_merchant_id(merchant_id)
        now = datetime.datetime.now()
        if now > activity['start_time'] and now < activity['end_time']:
            consume_money = int(consume_money) * activity['multiple']
            values['multiple'] = activity['multiple']
        recomender_values = {
            'gb': recomender['gb'] + int(consume_money),
            'total_gb': recomender['total_gb'] + int(consume_money),
            'consume_gb': recomender['consume_gb'] + int(consume_money)
        }
        db.customer_update_by_id(recomender['id'], recomender_values)
    return db.consume_create(values)


# 消费数量
def consume_count_by_id(merchant_id):
    return db.consume_count_by_merchant_id(merchant_id)


# 消费列表
def consume_list_by_merchant_id(merchant_id, page):
    consume_count = db.consume_count_by_merchant_id(merchant_id)
    page_num = consume_count/10 + 1 if consume_count % 10 else consume_count/10
    if page < 1 or page > page_num:
        return []
    temp = db.consume_list_by_merchant_id(merchant_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        consume_dict['num'] = count
        if consume_dict['customer_id']:
            recomender = db.customer_get_by_id(consume_dict['customer_id'])
            consume_dict['recomender'] = recomender['name']
        else:
            consume_dict['recomender'] = '无'
        consume_dict['consume_content'] = consume_dict['consume_content'] if consume_dict['consume_content'] else '无'
        consume_list.append(consume_dict)
        count += 1
    return consume_list[10*(page-1):10*page]


# 被查询消费数量
def search_consume_count(merchant_id, type, content):
    if type == '0':
        return db.search_consume_count_by_consumer_name(merchant_id, content)
    elif type == '1':
        customer = db.customer_get_by_serial_num(content)
        if not customer:
            return 0
        return db.search_consume_count_by_customer_id(merchant_id, customer['id'])
    elif type == '2':
        min_time = content + ' 00:00:00'
        max_time = content + ' 23:59:59'
        return db.search_consume_count_by_created_at(merchant_id, min_time, max_time)


# 被查询消费列表
def get_search_consume_list(merchant_id, page, type, content):
    consume_count = search_consume_count(merchant_id, type, content)
    if type == '0':
        temp = db.consume_list_by_consumer_name(merchant_id, content)
    elif type == '1':
        customer = db.customer_get_by_serial_num(content)
        if not customer:
            return []
        temp = db.consume_list_by_customer_id(merchant_id, customer['id'])
    elif type == '2':
        min_time = content + ' 00:00:00'
        max_time = content + ' 23:59:59'
        temp = db.consume_list_by_created_at(merchant_id, min_time, max_time)
    page_num = consume_count/10 + 1 if consume_count % 10 else consume_count/10
    if page < 1 or page > page_num:
        return []
    count = 1
    consume_list = []
    for consume in temp:
        consume_dict = dict(consume)
        consume_dict['num'] = count
        if consume_dict['customer_id']:
            recomender = db.customer_get_by_id(consume_dict['customer_id'])
            consume_dict['recomender'] = recomender['name']
        else:
            consume_dict['recomender'] = '无'
        consume_dict['consume_content'] = consume_dict['consume_content'] if consume_dict['consume_content'] else '无'
        consume_list.append(consume_dict)
        count += 1
    return consume_list[10*(page-1):10*page]


# 根据客户查找消费记录
def consume_list_by_customer_id(merchant_id, customer_id):
    temp = db.consume_list_by_customer_id(merchant_id, customer_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        consume_dict['num'] = count
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 根据客户查找消费记录
def consume_get_by_customer_id(customer_id):
    temp = db.consume_get_by_customer_id(customer_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        consume_dict['num'] = count
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 根据客户查找近期消费记录
def recent_consume_list_by_customer_id(customer_id):
    temp = db.consume_recent_list_by_customer_id(customer_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        consume_dict['num'] = count
        consume_list.append(consume_dict)
        count += 1
    return consume_list


# 根据客户查找消费记录
def consume_all_list_by_customer_id(customer_id):
    temp = db.consume_all_list_by_customer_id(customer_id)
    consume_list = []
    count = 1
    for consume in temp:
        consume_dict = dict(consume)
        consume_dict['num'] = count
        consume_list.append(consume_dict)
        count += 1
    return consume_list