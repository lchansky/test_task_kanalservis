from pprint import pprint

from db.DB import Database
from django_proj.main_app.google_api.config import RANGE
from django_proj.main_app.google_api.from_sheets import execute_data
from django_proj.main_app.utils import append_rub

DB_NAME = 'orders'
COLUMNS = ('id', 'order_number', 'price_usd', 'delivery_time', 'price_rub')


def main():
    Database.create_table(DB_NAME)
    data = execute_data(RANGE)
    append_rub(data)
    # pprint(data)
    Database.force_update(DB_NAME, COLUMNS, data)
    print('.......Data have been successfully loaded from Google to DB.........')


if __name__ == '__main__':
    main()
