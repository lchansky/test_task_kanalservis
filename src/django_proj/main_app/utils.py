import datetime
from typing import List, AnyStr

import requests
import xml.etree.ElementTree as ETree

CB_RF = 'http://www.cbr.ru/scripts/XML_daily.asp'
USD_COLUMN = 2
DATE_COLUMN = 3
COLUMNS_COUNT = 4


def append_rub(data: List[List]):
    """Принимает список списков из гугл таблицы, добавляет
        в каждый вложенный список цену в рублях"""
    rate = get_rate('USD')
    for elem in data:
        if len(elem) > USD_COLUMN:
            usd = float(elem[USD_COLUMN])
            elem.append(usd * rate)


def clean_date(data: List[List]):
    """Принимает список списков из гугл таблицы, форматирует
        дату в datetime obj в каждом вложенном списке"""
    for elem in data:
        if len(elem) > DATE_COLUMN:
            d = datetime.datetime.strptime(elem[DATE_COLUMN], '%d.%m.%Y')
            elem[DATE_COLUMN] = d


def get_rate(curr_from: AnyStr):
    """Принимает валюту (н-р "USD"), парсит XML страницу ЦБ РФ,
        возвращает курс этой валюты"""
    response = requests.get(CB_RF)
    root = ETree.fromstring(response.text)
    val = finder(curr_from, root)
    rate = float(val.find('Value').text.replace(',', '.'))
    nominal = float(val.find('Nominal').text.replace(',', '.'))
    return rate / nominal


def finder(curr, obj):
    """Рекурсивная функция для поиска валюты с нужным обозначением.
        Принимает curr - валюту и obj - объект <class 'xml.etree.ElementTree.Element'>.
        Возвращает объект типа ElementTree найденной валюты"""
    for elem in obj:
        if curr == elem.text:
            return obj
    else:
        for elem in obj:
            f = finder(curr, elem)
            if f is not None:
                return f


# def full_clean(data: List[List]):
#     """"""
#     for elem in data:
#         error = gen_error_message(elem)
#         if not error:
#             elem[DATE_COLUMN] = clean_date(elem[DATE_COLUMN])
#             elem.append(rub(elem[USD_COLUMN]))
#             elem.append('')
#         else:
#             temp = [None, 0, 0, datetime.date.today(), 0, error]
#             elem.clear()
#             elem.extend(temp)
#
#
# def int_or_none(s: AnyStr):
#     try:
#         return int(s)
#     except:
#         return None
#
#
# def kwargs_from_list(lst):
#     if lst[0]
#
#
# def gen_error_message(elem):
#     errors = []
#     if not int_or_none(elem[0]):
#         errors.append(f'Ошибка - некорректный №!')
#     if len(elem) < COLUMNS_COUNT:
#         errors.append(f'Ошибка - заполните все ячейки строки!')
#         return ' '.join(errors)
#     else:
#         if rub(elem[USD_COLUMN]) is False:
#             errors.append(f'Ошибка при обработке столбца стоимости!')
#         if clean_date(elem[DATE_COLUMN]) is False:
#             errors.append(f'Ошибка при обработке столбца даты!')
#     if errors:
#         return ' '.join(errors) + str(elem)
#     else:
#         return False
#
#
# def rub(amount_usd):
#     """Принимает сумму в USD, возвращает в рублях"""
#     rate = get_rate('USD')
#     try:
#         return float(amount_usd) * rate
#     except:
#         return False
#
#
# def clean_date(date):
#     """Принимает 'DD.MM.YYYY', возвращает datetime obj"""
#     try:
#         return datetime.datetime.strptime(date, '%d.%m.%Y')
#     except:
#         return False




















