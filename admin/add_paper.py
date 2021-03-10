#!/usr/bin/env python3

from util import DB
from conf import DB_FILENAME
import sys

if __name__ == '__main__':
    db = DB(DB_FILENAME)
    if len(sys.argv) > 4:
        print('usage: add_paper.py <title> <description> [url]')
    elif len(sys.argv) > 3:
        print(db.add_item(sys.argv[1], sys.argv[2], sys.argv[3]))
    elif len(sys.argv) > 2:
        print(db.add_item(sys.argv[1], sys.argv[2]))
    else:
        print('usage: add_paper.py <title> <description> [url]')
