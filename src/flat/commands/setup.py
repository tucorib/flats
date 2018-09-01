'''
Created on 31 aout 2018

@author: tuco
'''
import sys

from flat.configuration.sources import get_sources
from flat.services.sources import store_sources

if __name__ == '__main__':
    store_sources(get_sources())
    sys.exit(0)
