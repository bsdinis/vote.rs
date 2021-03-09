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

    def get_label_names(self, cursor = None) -> List[str]:
        cur = self.cursor(cursor)
        cur.execute('select id, name from label_names')

        return cur.fetchall()

    def get_labels(self, cursor = None) -> Dict[int, List[str]]:
        cur = self.cursor(cursor)
        cur.execute('''
        select item_id, name
            from labels join label_names on labels.label_id = label_names.id
            ''')

        d = defaultdict(lambda: list())
        for iid, name in cur.fetchall():
            d[iid].append(name)

        return d


    def list(self, cursor = None, show_done=False) -> List[Tuple[int, str, str, str, List[str]]]:
        cur = self.cursor(cursor)

        labels = self.get_labels(cur)
        if show_done:
            cur.execute('select id, title, body, url_link from items')
            return list(map(lambda x: x + (labels[x[0]], ), cur.fetchall()))
        else:
            cur.execute('select id, title, body, url_link from items where done = ?', (False, ))
            return list(map(lambda x: x + (labels[x[0]], ), cur.fetchall()))


    def add_label(self, name: str, cursor = None) -> int:
        cur = self.cursor(cursor)

        cur.execute('insert into label_names(name) values (?)', (name, ))
        id = cur.lastrowid

        self.conn.commit()
        return id

    def add_item(self, title: str, body: str, url_link: Optional[str], labels: List[str] = [], cursor = None) -> int:
        cur = self.cursor(cursor)
        cur.execute('select id, name from label_names')
        label_ids = {name: id for id, name in cur.fetchall()}
        cur.execute('insert into items(title, body, url_link, done) values (?, ?, ?, ?)', (title, body, url_link, False))

        id = cur.lastrowid
        for lbl in labels:
            cur.execute('insert into labels(label_id, item_id) values (?, ?)', (label_ids[lbl], id))

        self.conn.commit()
        return id

    def label_item(self, id: int, label: str, cursor = None):
        cur = self.cursor(cursor)

        cur.execute('select id from label_names where name=?', (label, ))
        ids = cur.fetchall()
        assert len(ids) <= 1
        label_id = self.add_label(label, cur) if len(ids) == 0 else ids[0][0]

        cur.execute('insert into labels(label_id, item_id) values (?, ?)', (label_id, id))
        self.conn.commit()

    def mark_done(self, id: int, cursor = None):
        cur = self.cursor(cursor)
        cur.execute('update items set done = ? where id = ?', (True, id))
        self.conn.commit()
