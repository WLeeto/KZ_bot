import telebot
import os
import time
from telebot import types
from courses import _get_courses, course_KZT

KZ_course = 7.1

def read_file(path):
    with open(path, "r") as token:
        return token.read()

bot = telebot.TeleBot(read_file("token.ini"))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Я умею быстро конвертировать валюты.\n"
                                      "Это очень помогает освоиться с новой валютой\n"
                                      "Примерно представить сколько что стоит в рублях")
    keep_going(message)

def keep_going(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_1 = types.KeyboardButton('Рубли в теньге')
    item_2 = types.KeyboardButton('Теньге в рубли')
    item_3 = types.KeyboardButton('Теньге в рубли по 7.1')
    item_4 = types.KeyboardButton('Разница между обменом по курсу и по 7.1 в теньге')

    markup.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, "Чем я могу помочь ?", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def input(message):
    if message.text == 'Рубли в теньге':
        bot.send_message(message.chat.id, "Конвертируем рубли в теньге по курсу ЦБ. Введите сумму в рублях:")
        bot.register_next_step_handler(message, convert_rub_to_kz_cb)
    elif message.text == 'Теньге в рубли':
        bot.send_message(message.chat.id, "Конвертируем теньге в рубли по курсу ЦБ. Введите сумму в теньге:")
        bot.register_next_step_handler(message, convert_kz_to_rub_cb)
    elif message.text == 'Теньге в рубли по 7.1':
        bot.send_message(message.chat.id, "Конвертируем теньге в рубли по курсу 7.1. Введите сумму в теньге:")
        bot.register_next_step_handler(message, convert_kz_to_rub_fix)
    elif message.text == 'Разница между обменом по курсу и по 7.1 в теньге':
        bot.send_message(message.chat.id, "Считаем разницу по обмену в теньге. Введи сумму в рублях:")
        bot.register_next_step_handler(message, count_kzt)
    else:
        bot.send_message(message.chat.id, "Такой команды я не знаю")
        keep_going(message)

def convert_rub_to_kz_cb(message):
    '''
    Рубли в теньге по курсу ЦБ
    '''
    try:
        bot.send_message(message.chat.id, f"{float(_replace(message.text))} рублей\nэто\n{round(float(_replace(message.text)) * course_KZT(), 1)} теньге")
        keep_going(message)
    except Exception:
        bot.send_message(message.chat.id, "Что то пошло не так\nвозможно вы ввели не число")
        keep_going(message)

def convert_kz_to_rub_cb(message):
    '''
    Теньге в рубли по курсу ЦБ
    '''
    try:
        bot.send_message(message.chat.id, f"{float(_replace(message.text))} теньге\nэто\n{round(float(_replace(message.text)) / course_KZT(), 1)} рублей")
        keep_going(message)
    except Exception:
        bot.send_message(message.chat.id, "Что то пошло не так\nвозможно вы ввели не число")
        keep_going(message)

def convert_kz_to_rub_fix(message):
    '''
    Теньге в рубли по 7.1 (самый частый курс)
    '''
    try:
        bot.send_message(message.chat.id, f"{float(_replace(message.text))} теньге\nэто\n{round(float(_replace(message.text)) / 7.1, 1)} рублей")
        keep_going(message)
    except Exception:
        bot.send_message(message.chat.id, "Что то пошло не так\nвозможно вы ввели не число")
        keep_going(message)

def count_kzt(message):
    '''
    Вывести разницу между обменом по курсу или по 7.1
    '''
    try:
        course = course_KZT()
        amount = float(message.text.replace(' ', ''))
        bot.send_message(message.chat.id, f"По курсу: {round(amount * course, 1)} теньге\n"
                                          f"По 7.1:      {round(amount * 7.1, 1)} теньге\n"
                                          f"Разница:  {round(amount * course - amount * 7.1, 1)} теньге")
        keep_going(message)
    except Exception:
        bot.send_message(message.chat.id, "Что то пошло не так\n"
                                          "Возможно вы ввели не число")
        keep_going(message)

def _replace(arg):
    replaced_arg = arg.replace(" ", "").replace(",", ".")
    return replaced_arg



bot.polling(none_stop=True)

