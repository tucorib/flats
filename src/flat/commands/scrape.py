'''
Created on 31 aout 2018

@author: tuco
'''
import sys

from flat.configuration.sources import get_sources
from flat.services.flats import register_flats
from flat.services.smtp import create_service, send_email
from flat.sources import build_source

if __name__ == '__main__':
    ads = []
    for source in get_sources():
        service = create_service()
        parser = build_source(source)
        try:
            parser.open()
            ads += register_flats(source, parser.parse())
        finally:
            parser.close()
    if len(ads) > 0:
        send_email(service, ads)
    sys.exit(0)
