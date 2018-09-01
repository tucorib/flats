'''
Created on 1 sept. 2018

@author: tuco
'''
from flat.services import open_db_connection


def register_flats(source, flats):
    conn = open_db_connection()
    cur = conn.cursor()
    for reference, url in flats:
        cur.execute("INSERT INTO flat (source_id, reference, url, date) SELECT source.id, '%s', '%s', current_timestamp FROM source WHERE source.name = '%s' AND NOT EXISTS (SELECT flat.id FROM source, flat WHERE source.name = '%s' AND flat.reference = '%s')" % (
            reference,
            url,
            source,
            source,
            reference)
        )
        if cur.rowcount == 1:
            yield (source, reference, url)
    conn.commit()
    conn.close()
