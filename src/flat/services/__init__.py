import psycopg2
from flat.configuration import db


def open_db_connection():
    return psycopg2.connect(
        host=db.get_db_host(),
        port=db.get_db_port(),
        database=db.get_db_name(),
        user=db.get_db_username(),
        password=db.get_db_password()
    )
