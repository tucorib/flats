'''
Created on 31 aout 2018

@author: tuco
'''
import sys

from flat.configuration.sources import get_sources
from flat.services.flats import register_flats
from flat.services.logger import logger
from flat.services.smtp import create_service, send_email
from flat.sources import build_source, build_browser

if __name__ == '__main__':
    ads = []
    browser = build_browser()
    try:
        for source in get_sources():
            parser = build_source(source, browser=browser)
            parser.open()
            ads += register_flats(source, parser.parse())
            parser.close()
    except Exception, error:
        logger.error(error)
    finally:
        if browser:
            browser.close()
    service = create_service()
    send_email(service, ads)
    sys.exit(0)
