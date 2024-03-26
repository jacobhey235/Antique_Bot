import telebot
from telebot import types
import json

bot = telebot.TeleBot("6286254023:AAF3bz8cBQNz2CbT5gzW5GQ0invtz9XAbco")
f = open('database.json')
database = json.load(f)
list_of_ids = []
for i in range(len(database[1]['content'])):
    for j in range(len(database[1]['content'][i]['products'])):
        list_of_ids.append(database[1]['content'][i]['products'][j]["id"])


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_buy = types.KeyboardButton(
        text="Купить")
    button_sell = types.KeyboardButton(
        text="Продать")
    keyboard.add(button_buy, button_sell)
    rm_id = keyboard.to_json()
    database[0]['content']['message_id'] = message.id
    database[0]['content']['chat_id'] = chat_id
    database[0]['content']['last_text'] = message.text
    database[0]['content']['last_markup'] = rm_id
    bot.send_message(chat_id,
                     'Добро пожаловать в бота онлайн-аукциона антикварных товаров. Выберите режим покупателя или '
                     'продавца',
                     reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text == 'Купить')
def buyer_menu(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cat0 = types.InlineKeyboardButton(text="Мебель",
                                      callback_data='furniture')
    cat1 = types.InlineKeyboardButton(text="Посуда",
                                      callback_data='dishes')
    cat2 = types.InlineKeyboardButton(text="Ювелирные изделия",
                                      callback_data='jewellery')
    cat3 = types.InlineKeyboardButton(text="Монеты",
                                      callback_data='coins')
    cat4 = types.InlineKeyboardButton(text="< Назад",
                                      callback_data='back')
    keyboard.add(cat0, cat1, cat2, cat3, cat4)
    rm_id = keyboard.to_json()
    database[0]['content']['message_id'] = message.id
    database[0]['content']['chat_id'] = chat_id
    database[0]['content']['last_text'] = message.text
    database[0]['content']['last_markup'] = rm_id
    bot.send_message(chat_id, 'Выберите категорию товаров:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda
        call: call.data == 'furniture' or call.data == 'dishes' or call.data == 'jewellery' or call.data == 'coins')
def select_product(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(database[1]['content'])):
        if database[1]['content'][i]['category'] == call.data:
            for j in range(len(database[1]['content'][i]['products'])):
                cat = types.InlineKeyboardButton(text=database[1]['content'][i]['products'][j]['name'],
                                                 callback_data=database[1]['content'][i]['products'][j]['id'])
                keyboard.add(cat)
    back = types.InlineKeyboardButton(text="< Назад",
                                      callback_data='back')
    keyboard.add(back)
    database[0]['content']['message_id'] = message.id
    database[0]['content']['chat_id'] = chat_id
    database[0]['content']['last_text'] = message.text
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Выберите товар из категории:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in list_of_ids)
def show_product(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.send_message(chat_id,
                     database[1]['content'][call.data // 10 - 1]['products'][call.data % 10 - 1]['name'],
                     reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_btn(call):
    bot.edit_message_text(chat_id=database[0]['content']['chat_id'], message_id=database[0]['content']['message_id'],
                          text=database[0]['content']['last_text'], reply_markup=database[0]['content']['last_markup'])


bot.polling(none_stop=True)
with open("database.json", "w") as outfile:
    json.dump(database, outfile)
f.close()
