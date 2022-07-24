import requests
import telebot

API_URL = 'http://localhost:8000/telegramAPI/'

bot = telebot.TeleBot('5494503233:AAHzKxMkF7t8ydGFv0qh-zjltUKNrEV8Ap0')


@bot.message_handler(commands=['start'])
def start(message):
    """Обрабатывает команду /start"""
    add_user(message.from_user.id)
    bot.send_message(
        message.from_user.id,
        'Привет. Я бот КаналСервиса. Я умею присылать уведомления о просроченных '
        'заказах и ошибках в заполнении таблицы.\nДавай познакомимся поближе, напиши /help'
    )


@bot.message_handler(commands=['on'])
def turn_on(message):
    """Обрабатывает команду /on - включает уведомления"""
    add_user(message.from_user.id)
    response = requests.post(API_URL,
                             data={'token': read_token(),
                                   'turn_on': message.from_user.id,
                                   })
    if response.status_code == 200:
        text = 'Уведомления включены. Чтобы выключить их, напиши /off'
    else:
        text = 'Ошибка. Включите сервер Django!'
    bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=['off'])
def turn_off(message):
    """Обрабатывает команду /off - выключает уведомления"""
    add_user(message.from_user.id)
    response = requests.post(API_URL,
                             data={'token': read_token(),
                                   'turn_off': message.from_user.id,
                                   })
    if response.status_code == 200:
        text = 'Уведомления отключены. Чтобы включить их обратно, напиши /on'
    else:
        text = 'Ошибка. Включите сервер Django!'
    bot.send_message(message.from_user.id, text)


@bot.message_handler()
def any_message(message):
    """Обрабатывает любые сообщения, в т.ч. /help"""
    add_user(message.from_user.id)
    bot.send_message(
        message.from_user.id,
        'Команды:\n/on - включить уведомления\n/off - выключить уведомления'
    )
    print(message.from_user.id)


def mass_messages(users_ids, message):
    """Рассылает message всем пользователям user_ids"""
    for user_id in users_ids:
        bot.send_message(user_id, message)


def read_token():
    """Читает токен из файла, он нужен для моего самодельного API"""
    with open('token.txt') as file:
        token = file.read()
    return token


def add_user(user_id):
    """Добавляет пользователя в БД, если его ещё там нет"""
    response = requests.post(API_URL,
                             data={'token': read_token(),
                                   'add_user': user_id,
                                   })
    if not response.status_code == 200:
        bot.send_message(user_id, 'Ошибка. Включите сервер Django!')


if __name__ == '__main__':
    print('Бот успешно запущен!')
    bot.infinity_polling()
