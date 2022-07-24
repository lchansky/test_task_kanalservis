from django.core.management.base import BaseCommand

from main_app.models import Order, User
from main_app.telegram_bot import bot


class Command(BaseCommand):
    help = 'Обновляет данные из гугл таблицы и записывает их в БД ' \
           'Отправляет уведомление в телеграм, если произошла ошибка'

    def handle(self, *args, **options):
        Order.refresh_table_infinity()
