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
    global presstrainbot
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

        strh = message.text
        str = message.text.lower()

        if (str.find('-')) >0:
            print(str.find('-'))
            qst = str[0:str.find('-')].strip()
            qst = qst.strip()
            ans = strh[str.find('-')+1:]
            ans = ans.strip()
            anslist = ans.split('.')
            ans = ''
            for val in anslist:
                ans += val.capitalize() + '. '



            print(qst)
            print(ans)
            try:
                qry = "select * from answer WHERE answer.question = '" + qst +  "';"
                answ_cursor.execute(qry)
                anser_list = answ_cursor.fetchall()
                print(len(anser_list))
                if len(anser_list) == 0:
                    qry = "insert into answer (question,answer,moderation,fio) " \
                          "values ('"+qst+"','"+ans+"',0,0)"
                    answ_cursor.execute(qry)
                    print()
                    sqlite_conn.commit()
                    mess = 'Мы молодцы!!! Ты хороший учитель. Мы выучили что-то новое.';
                    presstrainbot = 0
                else:
                    mess = 'Спасибо я уже знаю это';
                    presstrainbot = 0
                    print('add answer')
            except Exception as ex:
                print(ex)
            finally:
                print('add')


            print('подключились к ДБ')

        else:
            mess = 'Возможно вы не правильно поняли схему обучения. Напишите через "-"  по схеме "что вижу - что отвечаю"   '

        bot.send_message(message.chat.id, mess, parse_mode='html')

    except Exception as ex:
        print('Не получилось обучение')
        mess = 'Не получилось обучение';
        bot.send_message(message.chat.id, mess, parse_mode='html')
    finally:
        if (sqlite_conn):
            sqlite_conn.close()
            print('Мы молодцы!!! Ты хороший учитель. Мы выучили что-то новое.')


def speakbot(message):
    answerdb = 0
    print('text')
    try:
        sqlite_conn = sqlite3.connect('answer.db')
        mess_cursor = sqlite_conn.cursor()
        print('подключились к ДБ')
        messqst = message.text
        messqst = messqst.lower()
        messqst = messqst.strip()
        qry = "select * from answer WHERE answer.question = '" + messqst + "';"
        mess_cursor.execute(qry)
        anser_list = mess_cursor.fetchall()
        print(len(anser_list))
        if len(anser_list) == 0:
            print('я вас не понимаю. Попробуйте провести обчучение')
            mess = 'Я вас не понимаю. Попробуйте провести обучение /trainbot'
        else:
            row = anser_list[0]
            mess = row[1]
            if int(row[3]) == 1:
                mess = f'{mess}, <b>{message.from_user.first_name} <u> {message.from_user.last_name} </u></b>'

        bot.send_message(message.chat.id, mess, parse_mode='html')
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
            photo = open('hleb.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
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
        speakbot(message)

    print(message)


bot.polling(none_stop=True)


#     testaigul2022_bot


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
