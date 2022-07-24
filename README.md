# test_task_kanalservis
Тестовое задание для вакансии Python-разработчика в компании Каналсервис.

Склонируйте репозиторий.

```
docker-compose up
```

```
docker exec -d kanalservis python3 manage.py makemigrations
```

```
docker exec -d kanalservis python3 manage.py migrate
```

```
docker exec -d kanalservis python3 manage.py refresh_table
```

```
docker exec -d kanalservis python3 manage.py check_today_deadlines
```

```
docker exec -d kanalservis python3 manage.py check_expired_deadlines
```


```
docker exec -d -w /src/django_proj/main_app/telegram_bot/ kanalservis python3 bot.py
```

Далее откройте бота в телеграм https://t.me/kanalservis_test_task_bot, нажмите "Старт" и для включения уведомлений отправьте команду /on

В целях наглядности бот отправляет уведомления о просроченных заказах и об ошибках каждые 10 секунд.
Чтобы выключить уведомления, напишите /off




