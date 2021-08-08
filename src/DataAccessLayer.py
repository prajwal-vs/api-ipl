import logging
from os import environ

import psycopg2
from sqlalchemy.exc import SQLAlchemyError
from commons.json_utils import to_json

log_configs = {'database': environ.get('POSTGRES_DB'), 'user': environ.get('POSTGRES_USER'), 'password': '****',
               'host': environ.get('POSTGRES_SERVER'), 'port': 5432}

logger = logging.getLogger()


class DatabaseService:
    def __init__(self):
        self.client = psycopg2.connect(database=environ.get('POSTGRES_DB'), user=environ.get('POSTGRES_USER'),
                                       password=environ.get('POSTGRES_PASSWORD'), host=environ.get('POSTGRES_SERVER'),
                                       port=5432)
        self.db_session = self.client.cursor()

    def select_many(self, query):
        try:
            logger.info(f"Query: {query}")
            self.db_session.execute(query)
            result_set = self.db_session.fetchall()
            return result_set

        except SQLAlchemyError as e:
            logger.error(e)
            return to_json(str(e.__dict__['orig']).split('\n', 1)[0], is_error=True)

        finally:
            self.db_session.close()
