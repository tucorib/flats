'''
Created on 31 aout 2018

@author: tuco
'''
import sys

from flat.configuration.sources import get_sources
from flat.services.flats import register_flat
from flat.services.logger import logger
from flat.services.smtp import create_service, send_email
from flat.sources import build_source, build_browser

if __name__ == '__main__':
    ads = []
    browser = build_browser()
    try:
        for source in get_sources():
            try:
                parser = build_source(source, browser=browser)
                parser.open()
                for reference, url in parser.parse():
                    ad = register_flat(source, reference, url)
                    if ad:
                        ads.append(ad)
            except Exception, error:
                logger.error('[%s] %s' % (source, error))
            finally:
                parser.close()
    finally:
        if browser:
            browser.close()
    service = create_service()
    send_email(service, ads)
    sys.exit(0)
