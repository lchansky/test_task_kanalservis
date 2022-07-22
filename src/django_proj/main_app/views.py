from django.shortcuts import render

from main_app.models import Order


def main(request):
    Order.refresh_table()
    dates, sums = Order.get_sum_per_days()
    total_usd = Order.total_usd()
    orders = Order.objects.all()
    return render(request,
                  template_name='main.html',
                  context={
                      'dates': dates,
                      'sums': sums,
                      'total': total_usd,
                      'orders': orders,
                  })
