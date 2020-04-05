import covid
import telebot
import json
from telebot import types

covid = covid.Covid();
bot = telebot.TeleBot("1056202397:AAF6PBEj7-7nOVbmZ7bFdzIWUCsQwReKIYE");

def group(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 10)
    countries = covid.get_data();
    markup.add("World")
    for country in countries:
        countryName = country['country']
        btn = types.KeyboardButton(countryName)
        markup.add(btn)
    send_mes = f"<b>Hello {message.from_user.first_name}!</b>\n" \
        f"\tTo see current situation with COVID-19 " \
        f"\tin the World\n" \
        f"\tType or Select reference choice:\n" \
        f"\tPlease stay safe......."
    bot.send_message(message.chat.id, send_mes, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def mess(message):

    final_message = ""
    get_message_bot = message.text.strip().lower()
    if ( get_message_bot[len(get_message_bot)-1] == ' '):
        get_message_bot = get_message_bot[0:len(get_message_bot)-2]
    if ( get_message_bot[0] == ' '):
        get_message_bot = get_message_bot[1:]
    countries = covid.get_data();
    for country in countries:
        countryName = country['country']
        countryName = countryName
        if ( get_message_bot == countryName.lower() ):
             final_message += f"<u>Данные {countryName}:</u>\n" \
                 f"<b>Подтверждено : {country['confirmed']}</b>\n" \
                 f"<b>Смертей: {group(country['deaths'])}</b>\n" \
                 f"<b>Выздоровшие: {group(country['recovered'])}</b>\n"
    if get_message_bot == "world":
        final_message += f"<u>Данные World:</u>\n" \
            f"<b>Подтверждено : {group(covid.get_total_confirmed_cases())}</b>\n" \
            f"<b>Смертей: {group(covid.get_total_deaths())}</b>\n" \
            f"<b>Aктивные: {group(covid.get_total_active_cases())}</b>\n" \
            f"<b>Выздоровшие: {group(covid.get_total_recovered())}</b>\n"
    if final_message == "":
        final_message += f"<b>Неправильный ввод!!!</b>"

    bot.send_message(message.chat.id, final_message, parse_mode="html")

bot.polling(none_stop=True)

