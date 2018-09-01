import os

from pyhocon.config_parser import ConfigFactory

config = ConfigFactory.parse_file(os.getenv('FLAT_CONF', None))
