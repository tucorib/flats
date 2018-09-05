'''
Created on 1 sept. 2018

@author: tuco
'''

from flat.services import open_db_connection
from flat.services.logger import logger


def register_flat(source, reference, url):
    ad = None
    conn = open_db_connection()
    cur = conn.cursor()
    ad_count = 0
    cur.execute("INSERT INTO flat (source_id, reference, url, date) SELECT source.id, '%s', '%s', current_timestamp FROM source WHERE source.name = '%s' AND NOT EXISTS (SELECT flat.id FROM source, flat WHERE source.name = '%s' AND flat.reference = '%s')" % (
        reference,
        url,
        source,
        source,
        reference)
    )
    if cur.rowcount == 1:
        ad_count += 1
        ad = (source, reference, url)
    conn.commit()
    logger.debug('[%s] %d ad(s) stored' % (source, ad_count))
    conn.close()
    return ad