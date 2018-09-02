'''
Created on 2 sept. 2018

@author: tuco
'''
import logging
import logging.config
from flat.configuration.logging import get_logging_conf

logging.config.fileConfig(get_logging_conf())
logger = logging.getLogger('flats')