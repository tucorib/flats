'''
Created on 31 aout 2018

@author: tuco
'''
from flat.configuration import config


def get_logging_conf():
    return config.get('logging')
