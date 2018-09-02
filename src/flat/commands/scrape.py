'''
Created on 31 aout 2018

@author: tuco
'''
import sys

from flat.configuration.sources import get_sources
from flat.services.flats import register_flats
from flat.services.smtp import create_service, send_email
from flat.sources import build_source, build_browser

if __name__ == '__main__':
    ads = []
    browser = build_browser()
    try:
        for source in get_sources():
            service = create_service()
            parser = build_source(source, browser=browser)
            parser.open()
            ads += register_flats(source, parser.parse())
            parser.close()
    except Exception, e:
        print e
    finally:
        if browser:
            browser.close()
    if len(ads) > 0:
        send_email(service, ads)
    sys.exit(0)
