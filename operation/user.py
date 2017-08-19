# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import exception
from db import api as db


# 创建新用户
def create_user(username, password, role, created_at=None):
    if db.user_username_if_exist_in_db(username):
        raise exception.UserIsExistException()
    values = {
        'username': username,
        'password': password,
        'role': role,
        'created_at': created_at if created_at else None
    }
    return db.user_create(values)


# 根据username查找用户
def get_user_by_username(username):
    user = db.user_get_by_username(username)
    return dict(user)


# 登录
def login(username, password):
    ref = db.user_get_by_username(username)
    if not ref:
        raise exception.UserIsNotExistException()
    if ref['password'] == password:
        return dict(ref)
    else:
        raise exception.PasswordIsWrongException()


# 检查密码
def check_password(user_id, password):
    user = db.user_get_by_id(user_id)
    if user['password'] != password:
        raise exception.PasswordIsWrongException()


# 修改密码
def update_password(user_id, password):
    values = {
        'password': password
    }
    return db.user_update_by_id(user_id, values)

if __name__ == '__main__':
    create_user('manager', '123456', 1)
    print get_user_by_username('manager')