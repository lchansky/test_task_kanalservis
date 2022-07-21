from pprint import pprint

from db.DB import Database
from google_api.config import RANGE
from google_api.from_sheets import execute_data
from utils import append_rub

DB_NAME = 'orders'
COLUMNS = ('id', 'order_number', 'price_usd', 'delivery_time', 'price_rub')


def main():
    Database.create_table(DB_NAME)
    data = execute_data(RANGE)
    append_rub(data)
    pprint(data)
    Database.force_update(DB_NAME, COLUMNS, data)


if __name__ == '__main__':
    main()
