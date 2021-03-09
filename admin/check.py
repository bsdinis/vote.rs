#!/usr/bin/env python3

from util import DB
from conf import DB_FILENAME
if __name__ == '__main__':
    db = DB(DB_FILENAME)
    print('db@{} is OK')

    all = len(db.list(show_done = True))
    missing = len(db.list())
    print('{} papers to be read (total {})'.format(missing, all))

