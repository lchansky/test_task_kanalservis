from typing import List, AnyStr

import requests
import xml.etree.ElementTree as ETree

CB_RF = 'http://www.cbr.ru/scripts/XML_daily.asp'
AMOUNT_USD_COLUMN = 2


def append_rub(data: List[List]):
    """Принимает список списков из гугл таблицы, добавляет
    в каждый вложенный список цену в рублях"""
    rate = get_rate('USD')
    for elem in data:
        usd = float(elem[AMOUNT_USD_COLUMN])
        elem.append(usd * rate)


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


