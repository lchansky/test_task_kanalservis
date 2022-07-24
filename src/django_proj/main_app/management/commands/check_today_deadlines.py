from django.core.management.base import BaseCommand

from main_app.models import Order, User
from main_app.telegram_bot import bot


class Command(BaseCommand):
    help = 'Ищет в БД записи со сроком поставки сегодня и отправляет уведомление в телеграм, если находит'

    def handle(self, *args, **options):
        today_orders = Order.get_today_deadlines()
        users = User.get_users_with_notifications()
        if today_orders:
            bot.mass_messages(
                users,
                f'У вас есть заказы c конечным сроком поставки - сегодня!\n\n' + '\n'.join(today_orders)
            )
