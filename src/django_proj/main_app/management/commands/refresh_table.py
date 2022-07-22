from django.core.management.base import BaseCommand

from main_app.models import Order


class Command(BaseCommand):
    help = 'Обновляет данные из гугл таблицы и записывает их в БД'

    def handle(self, *args, **options):
        Order.refresh_table()
