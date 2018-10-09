'''
csvapi parser

CSV parser for csvapi
'''

import agate
import cchardet as chardet
import csv
import logging

__version__ = '0.1.0.dev'
__description__ = 'CSV parser for csvapi'


log = logging.getLogger(__name__)
block_size = 10


def detect_encoding(filepath):
    with open(filepath, 'rb') as f:
        return chardet.detect(f.read()).get('encoding')


def detect_dialect(filepath, encoding):
    lines = []
    with open(filepath, 'r', encoding=encoding) as csvfile:
        previous = []
        for idx, line in enumerate(csvfile):
            # stash line for next iteration
            if (idx + 1) % block_size:
                previous.append(line)
                continue
            else:
                lines += previous
                previous = []
                dialect = csv.Sniffer().sniff('\n'.join(lines))
                # not enough lines?
                if not dialect:
                    continue
                reader = csv.reader(lines, dialect=dialect)
                header = next(reader)
                # let's say all our CSVs have more than 1 column...
                if len(header) > 1:
                    log.debug('Found dialect at line %s with delimiter "%s"'
                              % (idx + 1, dialect.delimiter))
                    return dialect
        return


def get_table(filepath, encoding):
    dialect = detect_dialect(filepath, encoding)
    if dialect:
        try:
            return agate.Table.from_csv(filepath, dialect=dialect)
        except ValueError:
            pass
        try:
            dialect.doublequote = True
            return agate.Table.from_csv(filepath, dialect=dialect)
        except ValueError:
            pass
    return agate.Table.from_csv(filepath)


def parse(filepath, encoding=None):
    encoding = detect_encoding(filepath) if not encoding else encoding
    return get_table(filepath, encoding)
