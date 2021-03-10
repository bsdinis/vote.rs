'''
util.py
'''

import sqlite3 as sql

from typing import List, Tuple, Dict, Optional
from collections import defaultdict

class DB:
    def __init__(self, filename: str):
        self.conn = sql.connect(filename)


    def cursor(self, c = None):
        return c if c else self.conn.cursor()

    def list(self, cursor = None, show_done=False) -> List[Tuple[int, str, str, str, List[str]]]:
        cur = self.cursor(cursor)

        if show_done:
            cur.execute('select id, title, body, url_link from items')
            return cur.fetchall()
        else:
            cur.execute('select id, title, body, url_link from items where done = ?', (False, ))
            return cur.fetchall()

    def add_item(self, title: str, body: str, url_link: Optional[str] = None, cursor = None) -> int:
        cur = self.cursor(cursor)
        cur.execute('insert into items(title, body, url_link, done) values (?, ?, ?, ?)', (title, body, url_link, False))

        id = cur.lastrowid

        self.conn.commit()
        return id

    def mark_done(self, id: int, cursor = None):
        cur = self.cursor(cursor)
        cur.execute('update items set done = ? where id = ?', (True, id))
        self.conn.commit()
