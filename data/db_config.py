import psycopg2
import logging
from data.config import load_config

logging.config.fileConfig(fname='loggin.conf')
logger = logging.getLogger('simpleExample')

config = load_config(".env")


def get_db_connection():
    try:
        logger.info('Подключение к БД')
        conn = psycopg2.connect(config.db.uri)
        with conn.cursor() as cur:
            cur.execute(
                open("tables.sql", "r").read()
            )
        conn.commit()
        yield conn
    finally:
        logger.info('Отключение от БД')
        conn.close()
