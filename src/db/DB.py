from typing import List

from db.connector import db_connect


class Database:

    @staticmethod
    @db_connect
    def force_update(table: str, columns: tuple, data: List[List]):
        """Формирует текст запроса SQL для удаления старых данных и добавления новых"""
        cols = f'({", ".join(columns)})'
        values = (str(tuple(line)) for line in data)
        values = ',\n'.join(values)

        query = f'''
        BEGIN;
        DELETE FROM {table};
        INSERT INTO {table} {cols}
        VALUES {values};
        \nCOMMIT;
        '''
        return query

    @staticmethod
    @db_connect
    def delete_all(table: str):
        """Формирует текст запроса SQL для удаления данных из БД"""
        query = f'DELETE FROM {table};'
        return query

    @staticmethod
    @db_connect
    def create_table(table: str):
        """Формирует текст запроса SQL для создания таблицы"""
        query = f"""
            CREATE TABLE IF NOT EXISTS {table}(
            id serial PRIMARY KEY,
            order_number INT,
            price_usd DECIMAL,
            price_rub DECIMAL,
            delivery_time DATE);
        """
        return query





