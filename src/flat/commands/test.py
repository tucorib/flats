'''
Created on 31 aout 2018

@author: tuco
'''
import argparse
import sys

from flat.configuration.sources import get_sources
from flat.sources import build_source

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'sources',
        type=str,
        choices=get_sources(),
        nargs='+',
    )

    args = parser.parse_args()

    for source in args.sources:
        parser = build_source(source)
        try:
            parser.open()
            for reference, url in parser.parse():
                print '[%s] %s %s' % (
                    source,
                    reference,
                    url)
        finally:
            parser.close()
    sys.exit(0)
