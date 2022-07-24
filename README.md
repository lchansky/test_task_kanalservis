# test_task_kanalservis
Тестовое задание для вакансии Python-разработчика в компании Каналсервис.

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
docker exec -d -w /src/django_proj/main_app/telegram_bot/ kanalservis python3 bot.py
```





