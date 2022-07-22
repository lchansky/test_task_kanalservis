import telebot
bot = telebot.TeleBot('5494503233:AAHzKxMkF7t8ydGFv0qh-zjltUKNrEV8Ap0')


@bot.message_handler(commands=['start', 'help'])
def get_text_messages(message):
    bot.send_message(
        message.from_user.id,
        'Привет. Я бот КаналСервиса. Я буду присылать уведомления о просроченных '
        'заказах и ошибках в заполнении таблицы.'
    )


bot.infinity_polling()
