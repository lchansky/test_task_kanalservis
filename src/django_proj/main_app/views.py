from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main_app.models import Order, User


def main(request):
    """Отображает главную страницу"""
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


@csrf_exempt
def telegram_api(request):
    """Эта 'вьюха' нужна для общения Телеграм бота и Джанго по самодельному API"""
    if request.method == 'POST':
        post = request.POST
        with open('main_app/telegram_bot/token.txt') as file:
            token = file.read()
        if post.get('token') == token:
            if post.get('add_user'):
                User.add_user(post.get('add_user'))
            if post.get('turn_off'):
                User.disable_notifications(post.get('turn_off'))
            if post.get('turn_on'):
                User.enable_notifications(post.get('turn_on'))

        return JsonResponse({"ok": "POST request processed"})

    if request.method == 'GET':  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})
