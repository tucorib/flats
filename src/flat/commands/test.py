'''
Created on 31 aout 2018

@author: tuco
'''
import argparse
import logging
import logging.config
import sys

from flat.configuration.logging import get_logging_conf
from flat.configuration.sources import get_sources
from flat.sources import build_source, build_browser

logging.config.fileConfig(get_logging_conf())
logger = logging.getLogger('root')

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
                logger.info('[%s] %s %s' % (
                    source,
                    reference,
                    url
                ))
            parser.close()
    except Exception, error:
        logger.error(error)
    finally:
        if browser:
            browser.close()
    sys.exit(0)
