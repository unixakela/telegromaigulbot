import telebot
from telebot import types

# pip3 uninstall telebot
# pip3 uninstall PyTelegramBotAPI
# pip3 install pyTelegramBotAPI
# pip3 install --upgrade pyTelegramBotAPI

bot = telebot.TeleBot('5494582047:AAF6MZ07pdVjW5ApeYnQxFc7_-_gAxeZzR0')

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.InlineKeyboardMarkup()
    ammount_button = types.InlineKeyboardButton('Баланс',callback_data='Ammount')

    reply_ammount = markup.add(ammount_button)

    mess = f'Привет, <b>{message.from_user.first_name} <u> {message.from_user.last_name} </u></b>'

    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, 'Баланс', reply_markup=markup)

@bot.callback_query_handler(func= lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'Ammount':
        print(callback)
        print(callback.json.from.id)







@bot.message_handler()
def get_user_text(message):
    print(message.from_user.last_name +' '+message.from_user.first_name + " " + message.text)
    if message.text.lower() == 'привет' \
            or message.text == '👋'\
            or message.text == '🙋' \
            or message.text == '🖐' \
            or message.text == '✋' \
            or message.text == '🙋‍♀️' \
            or message.text == '🤚':
        mess = f'Привет, <b>{message.from_user.first_name} <u> {message.from_user.last_name} </u></b>'
        bot.send_message(message.chat.id, mess, parse_mode='html')
    elif message.text.lower() == 'ид':
        mess = f'Ваш ИД: <b>{message.from_user.id}></b>'
        bot.send_message(message.chat.id, mess, parse_mode='html')
    elif message.text.lower() == 'ква':
        mess = f'Ква-ква-ква!🐸🫒'
        bot.send_message(message.chat.id, mess, parse_mode='html')
    elif message.text.lower() == '🥨':
        mess = f'Приятного аппетита!🥨'
        bot.send_message(message.chat.id, mess, parse_mode='html')
    elif message.text.lower() == 'фото':
        photo = open('hleb.jpg','rb')
        bot.send_photo(message.chat.id,photo)
    else:
        mess = f'я тебя не понимаю!'
        bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id,message,parse_mode='html')


bot.polling(none_stop=True)


#     testaigul2022_bot


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
