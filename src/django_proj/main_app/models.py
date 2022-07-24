import datetime
from time import sleep

from django.db import models, transaction, IntegrityError
from django.db.models import Sum

from main_app.google_api.config import RANGE
from main_app.google_api.from_sheets import execute_data
from main_app.telegram_bot import bot
from main_app.utils import clean_date, append_rub

COLUMNS = ('pk', 'number', 'price_usd', 'delivery_time', 'price_rub')


class Order(models.Model):
    number = models.IntegerField(blank=True, null=True, verbose_name='Заказ №')
    price_usd = models.FloatField(blank=True, null=True, verbose_name='Стоимость, $')
    delivery_date = models.DateField(blank=True, null=True, verbose_name='Срок поставки')
    price_rub = models.FloatField(blank=True, null=True, verbose_name='Стоимость, Р')

    def __str__(self):
        return f'Заказ № {self.number} -- Срок поставки: {self.delivery_date} -- {self.price_usd} $'

    @staticmethod
    @transaction.atomic
    def refresh_table():
        """Обновляет БД теми данными, которые извлекаются из таблицы Google"""
        try:
            data = execute_data(RANGE)
            clean_date(data)
            append_rub(data)
            with transaction.atomic():
                Order.objects.all().delete()
                Order.objects.bulk_create(
                    [Order(
                        pk=line[0],
                        number=line[1],
                        price_usd=line[2],
                        delivery_date=line[3],
                        price_rub=line[4],
                    )
                        for line in data if line[0]]
                )
            print('Данные из гугл таблицы успешно '
                  'обновлены в Базу Данных!')
        except IntegrityError:
            error_text = 'Ошибка при добавлении данных в БД. Изменения не сохранены! '\
                         'Проверьте правильность указанных данных в таблице, и что все строки заполнены'
            bot.mass_messages(User.get_users_with_notifications(), error_text)
        except IndexError:
            error_text = 'Ошибка при обработке данных из таблицы! Изменения не сохранены! '\
                         'Проверьте, что все строки в таблице заполнены полностью'
            bot.mass_messages(User.get_users_with_notifications(), error_text)
        except:
            error_text = 'Ошибка! Изменения не сохранены! Проверьте токены, настройки доступа таблицы, правильная ли '\
                         'ссылка, правильность указанных данных в таблице, и что все строки заполнены корректно'
            bot.mass_messages(User.get_users_with_notifications(), error_text)

    @classmethod
    def get_sum_per_days(cls):
        """Возвращает две строки, даты и суммы заказов за каждую дату"""
        orders = cls.objects.values_list('delivery_date')
        orders = orders.annotate(total_price=Sum('price_usd'))
        orders = orders.order_by('delivery_date')

        dates, sums = zip(*list(orders))
        dates = str(list(
            dt.strftime("%d.%m.%Y") for dt in dates
        ))
        sums = str(list(sums))
        return dates, sums

    @classmethod
    def total_usd(cls):
        """Возвращает сумму USD всех заказов"""
        return cls.objects.aggregate(Sum('price_usd')).get('price_usd__sum')

    @classmethod
    def get_expired_deadlines(cls):
        """Ищет в БД записи с прошедшим сроком поставки"""
        orders_expired = cls.objects.filter(delivery_date__lt=datetime.date.today())
        return tuple(str(order) for order in orders_expired)

    @classmethod
    def get_today_deadlines(cls):
        """Ищет в БД записи с прошедшим сроком поставки"""
        orders_today = cls.objects.filter(delivery_date=datetime.date.today())
        return tuple(str(order) for order in orders_today)


class User(models.Model):
    """Эта модель нужна для удобства хранения списка пользователей, у которых включены уведомления в боте"""
    user_id = models.PositiveBigIntegerField()
    notifications = models.BooleanField(null=True)

    @classmethod
    def get_users_with_notifications(cls):
        """Возвращает кортеж из id пользователей, у которых включены уведомления"""
        users = cls.objects.filter(notifications=True).values_list('user_id', flat=True)
        return tuple(users)

    @classmethod
    def add_user(cls, user_id, notifications=None):
        """Добавляет пользователя в БД, если его ещё там нет"""
        if not cls.objects.filter(user_id=user_id):
            cls.objects.create(user_id=user_id, notifications=notifications)

    @classmethod
    def enable_notifications(cls, user_id):
        """Включает пользователю настройку уведомлений"""
        cls.objects.filter(user_id=user_id).update(notifications=True)

    @classmethod
    def disable_notifications(cls, user_id):
        """Выключает пользователю настройку уведомлений"""
        cls.objects.filter(user_id=user_id).update(notifications=False)
