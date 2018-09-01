'''
Created on 31 aout 2018

@author: tuco
'''
from flat.configuration import config


def get_smtp_host():
    return config.get('smtp.host')


def get_smtp_port():
    return config.get('smtp.port')


def get_smtp_secret():
    return config.get('smtp.secret')


def get_smtp_mail():
    return config.get('smtp.mail')


def get_smtp_password():
    return config.get('smtp.password')
