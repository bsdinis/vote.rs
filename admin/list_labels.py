#!/usr/bin/env python3

from util import DB
from conf import DB_FILENAME
import sys

if __name__ == '__main__':
    db = DB(DB_FILENAME)
    print('\n'.join('{:3}: {}'.format(id, name) for id, name in db.get_label_names()))
