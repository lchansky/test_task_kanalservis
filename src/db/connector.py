import psycopg2
from db.config import config


def db_connect(func):
    """
    Декоратор, который открывает соединение с БД перед выполнением
    функции, а после функции комиттит изменения и закрывает соединение.
    """
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = psycopg2.connect(**config)
            print('[INFO] Successfully connected to PostgreSQL')
            with connection.cursor() as cursor:
                # print('\n' + func(*args, **kwargs) + '\n')  # Вывод SQL запроса в терминал
                cursor.execute(func(*args, **kwargs))
                connection.commit()
                print('[INFO] Successfully committed PostgreSQL query')

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL:', _ex)
        finally:
            if connection:
                connection.close()
                print('[INFO] PostgreSQL connection closed')
    return wrapper
