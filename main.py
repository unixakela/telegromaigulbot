import telebot
from telebot import types

from balance import Balance
from config import tokenbot

import sqlite3


# pip3 uninstall telebot
# pip3 uninstall PyTelegramBotAPI
# pip3 install pyTelegramBotAPI
# pip3 install --upgrade pyTelegramBotAPI
import mysql
from mysql import Mysql


pressbalance = 0
presstrainbot=0

bot = telebot.TeleBot(tokenbot)

@bot.message_handler(commands=['start'])
def start(message):
    global pressbalance ,presstrainbot
    pressbalance = 0
    presstrainbot=0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    ammount_button = types.KeyboardButton('/баланс')
    start_button = types.KeyboardButton('/start')

    markup.add(ammount_button,start_button)

    mess = f'Привет, {message.from_user.first_name} {message.from_user.last_name} '



    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler(commands=['баланс','balance'])
def ammoiunt(message):
    global pressbalance,presstrainbot
    pressbalance = 1
    presstrainbot = 0
    bot.send_message(message.chat.id, 'Введите номер телефона', parse_mode='html')

@bot.message_handler(commands=['trainbot'])
def ammoiunt(message):
    global pressbalance,presstrainbot
    pressbalance = 0
    presstrainbot = 1
    bot.send_message(message.chat.id, 'Научите меня новым дилогам:) вопрос - ответ', parse_mode='html')





@bot.callback_query_handler(func= lambda callback: callback.data)
def check_callback_data(callback, mysql=None):
    if callback.data == 'Ammount':
        chekmysql = Mysql

        Mysql.create_connectio_mysql_db(chekmysql)
        Mysql.create_cursor_mysql_db(chekmysql)
        print(chekmysql.connection_db)
        print(chekmysql.cursor)

        print(callback)
        print(callback.from_user.id)
        print(callback.json)
        Mysql.close(chekmysql)
        bot.send_message(callback.from_user.id,'Введите номер телефона',parse_mode='html')


# @bot.message_handler(content_types=['text'])
# def mess(message):
#     final_message = ''
#     get_message_bot  = message.text.strip().lower()


def speakbalance(message):
    global pressbalance
    mess = message.text
    balanc = Balance()
    client = balanc.findclient(mess)
    print(client)
    print(balanc.get_balance(client))
    if len(client) > 0:
        mess = 'Ваш баланс составляет ' + str(balanc.get_balance(client)) + ' бонусных баллов!'
        pressbalance = 0
    else:
        mess = "клиент с таким номером не зарегестрирован, проверьте правильность веденных данных"
    bot.send_message(message.chat.id, mess, parse_mode='html')

    print(message.from_user.last_name + ' ' + message.from_user.first_name + " " + message.text)


def speaktrainbot(message):
    try:
        sqlite_conn = sqlite3.connect('answer.db')
        answ_cursor = sqlite_conn.cursor()
        # попытка создать таблицу с ответами
        try:
            qry = "CREATE table IF NOT EXISTS answer (question TEXT NOT NULL, answer TEXT NOT NULL, moderation INT, fio INT)"
            answ_cursor.execute(qry)
            print('Таблицу создали')
        except Exception as ex:
            print(Exception)
        finally:
            print('все ок или не ок')


        print(message)

        # try:
        #     qry = "CREATE table IF NOT EXISTS answer (question TEXT NOT NULL, answer TEXT NOT NULL, moderation INT, fio INT)"
        #     answ_cursor.execute(qry)
        #     print('Таблицу создали')
        # except Exception as ex:
        #     print(Exception)
        # finally:
        #     print('все ок или не ок')
        strh = message.text
        str = message.text.lower()

        print(str.find('-'))
        qst = str[0:str.find('-')].strip()
        qst.strip()
        ans = strh[str.find('-')+1:]
        ans.strip()
        print(qst)
        print(ans)
        print('подключились к ДБ')
    except Exception as ex:
        print('Не получилось обучение')
    finally:
        if (sqlite_conn):
            sqlite_conn.close()
            print('Мы молодцы!!! Ты хороший учитель. Мы выучили что-то новое.')



@bot.message_handler()
def get_user_text(message):
    global pressbalance,presstrainbot
    print(pressbalance)
    print(presstrainbot)
    if pressbalance == 1:
         speakbalance(message)
    elif presstrainbot == 1:
        speaktrainbot(message)

    else:
        answerdb=0
        print('text')
        try:
            sqlite_conn = sqlite3.connect('answer.db')
            answ_cursor = sqlite_conn.cursor()
            print('подключились к ДБ')
        except Exception as ex:
            print(ex)

            if message.text.lower() == 'привет' \
                    or message.text == '👋' \
                    or message.text == 'hi' \
                    or message.text == 'hello' \
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
                # elif message.text.lower() == 'баланс':
                #     mess = f'Введите номер телефона'
                #     bot.send_message(message.chat.id, mess, parse_mode='html')
            else:
                mess = f'я тебя не понимаю!'
                bot.send_message(message.chat.id, mess, parse_mode='html')
                # bot.send_message(message.chat.id, message, parse_mode='html')
        finally:
            if (sqlite_conn):
                sqlite_conn.close()
    print(message)


bot.polling(none_stop=True)


#     testaigul2022_bot


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
