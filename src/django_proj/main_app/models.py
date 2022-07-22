from django.db import models, transaction, IntegrityError
from django.db.models import Sum

from main_app.google_api.config import RANGE
from main_app.google_api.from_sheets import execute_data
from main_app.utils import clean_date, append_rub

COLUMNS = ('pk', 'number', 'price_usd', 'delivery_time', 'price_rub')


class Order(models.Model):
    number = models.IntegerField(blank=True, null=True, verbose_name='Заказ №')
    price_usd = models.FloatField(blank=True, null=True, verbose_name='Стоимость, $')
    delivery_date = models.DateField(blank=True, null=True, verbose_name='Срок поставки')
    price_rub = models.FloatField(blank=True, null=True, verbose_name='Стоимость, Р')

    @staticmethod
    @transaction.atomic
    def refresh_table():
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
            print('Ошибка при добавлении данных в БД. Изменения не сохранены! '
                  'Проверьте правильность указанных данных в таблице, и что все строки заполнены'
                  )
        except IndexError:
            print('Ошибка при обработке данных из таблицы! Изменения не сохранены! '
                  'Проверьте, что все строки в таблице заполнены полностью'
                  )
        except:
            print('Ошибка! Изменения не сохранены! Проверьте токены, настройки доступа таблицы, правильная ли ссылка, '
                  'правильность указанных данных в таблице, и что все строки заполнены корректно'
                  )

    @staticmethod
    def get_sum_per_days():
        orders = Order.objects.values_list('delivery_date')
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
