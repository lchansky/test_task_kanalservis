from time import sleep

from django.core.management.base import BaseCommand

from main_app.models import Order, User
from main_app.telegram_bot import bot


class Command(BaseCommand):
    help = 'Ищет в БД записи с прошедшим сроком поставки и отправляет уведомление в телеграм, если находит'

    def handle(self, *args, **options):
        while True:
            expired_orders = Order.get_expired_deadlines()
            users = User.get_users_with_notifications()
            if expired_orders:
                bot.mass_messages(
                    users,
                    f'У вас есть просроченные заказы!\n\n' + '\n'.join(expired_orders)
                )
            sleep(10)
