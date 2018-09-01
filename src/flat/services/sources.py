'''
Created on 31 aout 2018

@author: tuco
'''
from flat.services import open_db_connection


def get_sources():
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM source ORDER BY name;')
    for _ in cur.fetchall():
        yield _
    conn.close()


def store_sources(sources):
    conn = open_db_connection()
    cur = conn.cursor()
    for source in sources:
        cur.execute("INSERT INTO source (name) SELECT '%s' WHERE NOT EXISTS (SELECT name FROM source WHERE name = '%s');" % (source, source))
    conn.commit()
    conn.close()
