#!/usr/bin/env python3

from util import DB
from conf import DB_FILENAME
if __name__ == '__main__':
    db = DB(DB_FILENAME)
    print('\n'.join('{:3} |>\t\'{}\''.format(x[0], x[1]) for x in db.list()))
