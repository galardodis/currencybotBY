import telebot
import time
from telebot import types
from tokens import TELE_TOKEN
from extensions_by import CryptoConverter, APIException, currencie
from background import keep_alive  # постоянный онлайн

# import bot_app_world

bot = telebot.TeleBot(TELE_TOKEN)

ls = []


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Курсы валют')
    btn2 = types.KeyboardButton('Конвертация')
    markup.add(btn1, btn2)
    text = 'Привет! Я Бот-Конвертер валют и я могу:  \n\n' \
           '- Показать курсы валют по отношению к белорусскому рублю (Кнопка "Курсы валют")' \
           '\n\n- Конвертировать валюты (кнопка "Конвертация")' \
           '\n\nНапомнить, что я могу через команду: /help'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['help'])
def helpp(message: telebot.types.Message):
    text = 'Я могу:  \n\n' \
           '- Показать курсы валют по отношению к белорусскому рублю (Кнопка "Курсы валют")' \
           '\n\n- Конвертировать валюты (кнопка "Конвертация")' \
           '\n\n' \
           'Напомнить, что я могу через команду: /help'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['course'])
def course(message: telebot.types.Message):
    text = 'Курсы валют на сегодня:'
    for key in currencie:
        text = '\n'.join((text, f'{currencie[key][0]} {currencie[key][1]} ({key}) = {currencie[key][2]} BYN'))
    text += f'\n\nПо курсу НБ РБ на {time.strftime("%d %b %Y %H:%M:%S")}'
    text += '\n\nНапомнить, что я могу через команду: /help'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    if message.text == 'Курсы валют':
        text = 'Курсы валют на сегодня:'
        for key in currencie:
            text = '\n'.join((text, f'{currencie[key][0]} {currencie[key][1]} ({key}) = {currencie[key][2]} BYN'))
        text += f'\n\nПо курсу НБ РБ на {time.strftime("%d %b %Y %H:%M:%S")}'
        text += '\n\nНапомнить, что я могу через команду: /help'
        bot.send_message(message.chat.id, text)

    elif message.text == 'Конвертация':
        bot.send_message(message.chat.id, 'Введите сумму конвертации')

    elif message.text.isdigit() and len(ls) == 0:
        ls.append(int(message.text))
        markup = types.InlineKeyboardMarkup()
        for key in currencie:
            markup.add(types.InlineKeyboardButton(
                f'{currencie[key][3]} ({key})', callback_data=key))
        bot.send_message(message.chat.id, 'Доступные валюты:', reply_markup=markup)
        bot.send_message(message.chat.id, 'Выберите валюту конвертации из представленных выше')
    else:
        ls.clear()
        bot.send_message(message.chat.id, 'Введите сумму конвертации')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if len(ls) == 0:
        bot.send_message(callback.message.chat.id, 'Введате сумму конвертации')
    elif len(ls) < 2:
        ls.append(callback.data)
        bot.send_message(callback.message.chat.id, f'Вы выбрали {currencie[callback.data][3]} ({callback.data})')
        bot.send_message(callback.message.chat.id, f'Выберите валюту в которую конвертируем из представленных выше')
    elif len(ls) == 2:
        bot.send_message(callback.message.chat.id, f'Вы выбрали {currencie[callback.data][3]} ({callback.data})')
        ls.append(callback.data)

        amount, quote, base = ls
        total_base = CryptoConverter.get_price(quote, base, amount)
        text = f'{amount} {quote} = {total_base} {base}\n' \
               f'По курсу НБ РБ на {time.strftime("%d %b %Y %H:%M:%S")}'
        bot.send_message(callback.message.chat.id, text)
        ls.clear()


# keep_alive() #постоянный онлайн
# if __name__ == '__main__':
bot.polling()
