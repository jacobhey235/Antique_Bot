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
database[0]['chats_data'].clear()


@bot.message_handler(commands=['start'])
def welcome(message):
    '''
    Функция, срабатывающая в начале работы бота
    '''
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_buy = types.KeyboardButton(
        text="Купить")
    button_sell = types.KeyboardButton(
        text="Продать")
    keyboard.add(button_buy, button_sell)
    rm_id = keyboard.to_json()
    database[0]['chats_data'][str(chat_id)] = {}
    database[0]['chats_data'][str(message.chat.id)]['last_img_message'] = 0
    database[0]['chats_data'][str(chat_id)]['message_id'] = message.id
    database[0]['chats_data'][str(chat_id)]['last_text'] = [message.text]
    database[0]['chats_data'][str(chat_id)]['last_markup'] = [rm_id]
    bot.send_message(chat_id,
                     'Добро пожаловать в бота онлайн-аукциона антикварных товаров. Выберите режим покупателя или '
                     'продавца',
                     reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text == 'Купить')
def buyer_menu(message):
    chat_id = message.chat.id
    a = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, 'Вы выбрали режим покупателя', reply_markup=a)
    database[0]['chats_data'][str(chat_id)]['message_id'] = message.id
    database[0]['chats_data'][str(chat_id)]['last_text'].append(message.text)
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
    database[0]['chats_data'][str(chat_id)]['message_id'] = message.id
    database[0]['chats_data'][str(chat_id)]['last_text'].append(message.text)
    database[0]['chats_data'][str(chat_id)]['last_markup'].append(rm_id)
    bot.send_message(chat_id, 'Выберите категорию товаров:', reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text == 'Продать')
def seller_menu(message):
    chat_id = message.chat.id
    a = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, 'Вы выбрали режим продавца', reply_markup=a)
    database[0]['chats_data'][str(chat_id)]['message_id'] = message.id
    database[0]['chats_data'][str(chat_id)]['last_text'].append(message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for product_id in list_of_ids:
        if str(product_id) in database[2]['content'][str(chat_id)]:
            product = types.InlineKeyboardButton(text=database[2]['content'][str(chat_id)][str(product_id)]['name'],
                                                 callback_data=str(product_id))
            keyboard.add(product)
    button_add = types.InlineKeyboardButton(
        text="Добавить товар", callback_data='add_product')
    keyboard.add(button_add)
    back = types.InlineKeyboardButton(text="< Назад", callback_data="back")
    keyboard.add(back)
    if len(database[2]['content'][str(chat_id)]):
        bot.send_message(chat_id, 'Список ваших товаров:', reply_markup=keyboard)
    else:
        bot.send_message(chat_id, 'У вас нет товаров. Добавьте их', reply_markup=keyboard)
    rm_id = keyboard.to_json()
    database[0]['chats_data'][str(chat_id)]['message_id'] = message.id
    database[0]['chats_data'][str(chat_id)]['last_text'].append(message.text)
    database[0]['chats_data'][str(chat_id)]['last_markup'].append(rm_id)


@bot.callback_query_handler(func=lambda
        call: call.data == 'add_furniture' or call.data == 'add_dishes' or call.data == 'add_jewellery' or call.data == 'add_coins')
def add_product_category(call):
    chat_id = call.message.chat.id
    database[0]['chats_data'][str(chat_id)]['message_id'] = call.message.id
    database[0]['chats_data'][str(chat_id)]['last_text'].append(call.message.text)
    for k in range(len(list_of_ids)):
        if call.data == 'add_furniture' and list_of_ids[k] % 10 == 2:
            database[2]['content'][str(chat_id)][str(list_of_ids[k - 1] + 1)] = {}
            break
        if call.data == 'add_dishes' and list_of_ids[k] % 10 == 3:
            database[2]['content'][str(chat_id)][str(list_of_ids[k - 1] + 1)] = {}
            break
        if call.data == 'add_jewellery' and list_of_ids[k] % 10 == 4:
            database[2]['content'][str(chat_id)][str(list_of_ids[k - 1] + 1)] = {}
            break
        if call.data == 'add_coins' and k == len(list_of_ids) - 1:
            database[2]['content'][str(chat_id)][str(list_of_ids[k] + 1)] = {}
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Введите название товара:', reply_markup=None)
    bot.register_next_step_handler(call.message, get_product_name)


def get_product_name(message):
    chat_id = message.chat.id
    for elem in list_of_ids:
        if str(elem) in database[2]['content'][str(chat_id)]:
            if not (len(database[2]['content'][str(chat_id)][str(elem)])):
                database[2]['content'][str(chat_id)][str(elem)]["name"] = message.text
                break
    bot.send_message(chat_id, 'Введите сумму минимальной ставки в долларах:', reply_markup=None)
    bot.register_next_step_handler(message, get_minimum_bid)


def get_minimum_bid(message):
    chat_id = message.chat.id
    for elem in list_of_ids:
        if str(elem) in database[2]['content'][str(chat_id)]:
            database[2]['content'][str(chat_id)][str(elem)]["min_bid"] = int(message.text)
            database[2]['content'][str(chat_id)][str(elem)]["cur_bid"] = int(message.text)
            break
    bot.send_message(chat_id, 'Введите сумму минимальной ставки в долларах:', reply_markup=None)
    # bot.register_next_step_handler(message, get_product_name)


@bot.callback_query_handler(func=lambda call: call.data == 'add_product')
def add_product(call):
    chat_id = call.message.chat.id
    database[0]['chats_data'][str(chat_id)]['message_id'] = call.message.id
    database[0]['chats_data'][str(chat_id)]['last_text'].append(call.message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cat0 = types.InlineKeyboardButton(text="Мебель",
                                      callback_data='add_furniture')
    cat1 = types.InlineKeyboardButton(text="Посуда",
                                      callback_data='add_dishes')
    cat2 = types.InlineKeyboardButton(text="Ювелирные изделия",
                                      callback_data='add_jewellery')
    cat3 = types.InlineKeyboardButton(text="Монеты",
                                      callback_data='add_coins')
    cat4 = types.InlineKeyboardButton(text="< Назад",
                                      callback_data='back')
    keyboard.add(cat0, cat1, cat2, cat3, cat4)
    rm_id = keyboard.to_json()
    database[0]['chats_data'][str(chat_id)]['message_id'] = call.message.id
    database[0]['chats_data'][str(chat_id)]['last_text'].append(call.message.text)
    database[0]['chats_data'][str(chat_id)]['last_markup'].append(rm_id)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Выберите категорию товаров', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda
        call: call.data == 'furniture' or call.data == 'dishes' or call.data == 'jewellery' or call.data == 'coins')
def select_product_buyer(call):
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
    rm_id = keyboard.to_json()
    database[0]['chats_data'][str(chat_id)]['message_id'] = message.id
    database[0]['chats_data'][str(chat_id)]['last_text'].append(message.text)
    database[0]['chats_data'][str(chat_id)]['last_markup'].append(rm_id)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Выберите товар из категории:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_btn(call):
    if database[0]['chats_data'][str(call.message.chat.id)]['last_markup']:
        database[0]['chats_data'][str(call.message.chat.id)]['last_markup'].pop()
    if not (database[0]['chats_data'][str(call.message.chat.id)]['last_text'][
                len(database[0]['chats_data'][str(call.message.chat.id)]['last_text']) - 1] == 'Купить' or
            database[0]['chats_data'][str(call.message.chat.id)]['last_text'][
                len(database[0]['chats_data'][str(call.message.chat.id)]['last_text']) - 1] == 'Продать'):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=database[0]['chats_data'][str(call.message.chat.id)]['message_id'],
                              text=database[0]['chats_data'][str(call.message.chat.id)]['last_text'][
                                  len(database[0]['chats_data'][str(call.message.chat.id)]['last_text']) - 1],
                              reply_markup=database[0]['chats_data'][str(call.message.chat.id)]['last_markup'][
                                  len(database[0]['chats_data'][str(call.message.chat.id)]['last_markup']) - 1])
        if database[0]['chats_data'][str(call.message.chat.id)]['last_img_message'] and \
                call.message.chat.id and \
                database[0]['chats_data'][str(call.message.chat.id)]['last_text'][len(
                    database[0]['chats_data'][str(call.message.chat.id)][
                        'last_text']) - 1] == 'Выберите товар из категории:':
            bot.delete_message(message_id=database[0]['chats_data'][str(call.message.chat.id)]['last_img_message'],
                               chat_id=call.message.chat.id)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_buy = types.KeyboardButton(
            text="Купить")
        button_sell = types.KeyboardButton(
            text="Продать")
        keyboard.add(button_buy, button_sell)
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=database[0]['chats_data'][str(call.message.chat.id)]['message_id'])
        database[0]['chats_data'][str(call.message.chat.id)]['last_img_message'] = 0
        bot.send_message(chat_id=call.message.chat.id,
                         text='Добро пожаловать в бота онлайн-аукциона антикварных товаров. Выберите режим покупателя '
                              'или '
                              'продавца',
                         reply_markup=keyboard)

    database[0]['chats_data'][str(call.message.chat.id)]['last_text'].pop()


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = 'product_images/' + file_info.file_unique_id + '.jpg'
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, 'Фотография сохранена.')


@bot.callback_query_handler(func=lambda call: int(call.data) in list_of_ids)
def show_product_buyer(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    rm_id = keyboard.to_json()
    database[0]['chats_data'][str(call.message.chat.id)]['last_text'].append(message.text)
    database[0]['chats_data'][str(call.message.chat.id)]['last_markup'].append(rm_id)
    cat0 = types.InlineKeyboardButton(text="Сделать ставку",
                                      callback_data='bid')
    cat1 = types.InlineKeyboardButton(text="Заказать экспертизу",
                                      callback_data='get_expert')
    cat2 = types.InlineKeyboardButton(text="< Назад",
                                      callback_data='back')
    keyboard.add(cat0, cat1, cat2)
    if database[1]['content'][int(call.data) // 10 - 1]['products'][int(call.data) % 10][
        'photo_url']:
        img = open(database[1]['content'][int(call.data) // 10 - 1]['products'][int(call.data) % 10][
                       'photo_url'], 'rb')
        photo_message = bot.send_photo(chat_id=chat_id, photo=img)
        database[0]['chats_data'][str(call.message.chat.id)]['last_img_message'] = photo_message.id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Название товара: ' +
                               database[1]['content'][int(call.data) // 10 - 1]['products'][int(call.data) % 10][
                                   'name'] + '\nТекущая ставка: ' + str(
                              database[1]['content'][int(call.data) // 10 - 1]['products'][int(call.data) % 10][
                                  'cur_bid']) + '\nНачало торгов: ' +
                               database[1]['content'][int(call.data) // 10 - 1]['products'][int(call.data) % 10][
                                   'bid_start'], reply_markup=keyboard)


bot.polling(none_stop=True)
with open("database.json", "w") as outfile:
    json.dump(database, outfile)
f.close()
