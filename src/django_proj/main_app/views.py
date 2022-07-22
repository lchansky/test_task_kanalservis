from django.shortcuts import render

from main_app.models import Order


def main(request):
    Order.refresh_table()
    return render(request, 'main.html')
