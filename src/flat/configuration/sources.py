'''
Created on 31 aout 2018

@author: tuco
'''
from flat.configuration import config


def get_sources():
    return config.get('sources').keys()


def get_source_class(source):
    return config.get('sources.%s.class' % source)


def get_source_options(source):
    return config.get('sources.%s.options' % source)
