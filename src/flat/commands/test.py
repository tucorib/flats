'''
Created on 31 aout 2018

@author: tuco
'''
import argparse
import sys

from flat.configuration.sources import get_sources
from flat.sources import build_source, build_browser

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'sources',
        type=str,
        choices=get_sources(),
        nargs='+',
    )

    args = parser.parse_args()

    browser = build_browser()
    try:
        for source in args.sources:
            parser = build_source(source, browser=browser)
            parser.open()
            for reference, url in parser.parse():
                print '[%s] %s %s' % (
                    source,
                    reference,
                    url)
            parser.close()
    except Exception, e:
        print e
    finally:
        if browser:
            browser.close()
    sys.exit(0)
