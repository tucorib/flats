'''
Created on 31 aout 2018

@author: tuco
'''
from flat.configuration import config


def get_db_host():
    return config.get('db.host')


def get_db_port():
    return config.get('db.port')


def get_db_name():
    return config.get('db.name')


def get_db_username():
    return config.get('db.username')


def get_db_password():
    return config.get('db.password')
