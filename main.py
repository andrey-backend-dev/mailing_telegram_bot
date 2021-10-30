from pprint import pprint

import telebot
import os
import json
from dotenv import load_dotenv
from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.connection_cext import CMySQLConnection
from typing import Optional
import mysql.connector
from database import connect_mysql, disconnect_mysql, commit


load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
with open(file="commands.json", mode="r", encoding="utf-8") as commands_json:
    json_file = json.load(commands_json)



@bot.message_handler(commands=['start'])
def start(message):
    try:
        cursor = connect_mysql()
        user = message.from_user
        cursor.execute(f'SELECT id FROM users where id = {user.id}')
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        print(f'Failed selecting user id\n{err}')
    else:
        if not result:
            cursor.execute(f'INSERT INTO users (id, username) VALUES ({user.id}, "{user.username}")')
            commit()
    finally:
        disconnect_mysql()
    language(message, first=True)


@bot.message_handler(commands=['language'])
def language(message, first: bool = False):
    markup = telebot.types.InlineKeyboardMarkup()
    if first:
        markup.add(telebot.types.InlineKeyboardButton(text='English', callback_data="en|first"))
        markup.add(telebot.types.InlineKeyboardButton(text='Русский', callback_data="ru|first"))
    else:
        markup.add(telebot.types.InlineKeyboardButton(text='English', callback_data="en"))
        markup.add(telebot.types.InlineKeyboardButton(text='Русский', callback_data="ru"))

    bot.send_message(message.chat.id, text="Choose your language/Выберите свой язык:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    call_data = call.data.split('|')
    lang = call_data[0]
    try:
        cursor = connect_mysql()
        cursor.execute(f"UPDATE users SET language = '{lang}' WHERE id = {call.from_user.id}")
        commit()
    except mysql.connector.Error as err:
        print(f'Failed changing language.\n{err}')
        if lang == 'ru':
            bot.answer_callback_query(callback_query_id=call.id, text='Ошибка.')
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Error.')
    else:
        if lang == 'ru':
            bot.answer_callback_query(callback_query_id=call.id, text='Язык успешно сменен!')
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Language successfully changed!')
        if len(call_data) != 1:
            info(call, True)
    finally:
        disconnect_mysql()


@bot.message_handler(commands=['help'])
def help_user(message):
    try:
        cursor = connect_mysql()
        cursor.execute(f"SELECT language FROM users WHERE id = {message.from_user.id}")
        lang = cursor.fetchone()[0]
    except mysql.connector.Error as err:
        print(f'Failed in help_user block.{err}')
        bot.send_message(message.chat.id, 'Error')
    else:
        answer: str = ''
        for command in json_file[lang]['common_user_commands']:
            answer += f'/{command}: {json_file[lang]["common_user_commands"][command]}\n'
        bot.reply_to(message, answer)
    finally:
        disconnect_mysql()


@bot.message_handler(commands=['info'])
def info(message, first: bool = False):
    try:
        cursor = connect_mysql()
        cursor.execute(f'SELECT language FROM users WHERE id = {message.from_user.id}')
        lang = cursor.fetchone()[0]
    except mysql.connector.Error as err:
        print(f'Failed in info block.\n{err}')
    else:
        if first:
            bot.send_message(message.message.json['chat']['id'], json_file[lang]['greetings'])
        else:
            bot.send_message(message.chat.id, json_file[lang]['greetings'])
    finally:
        disconnect_mysql()

if __name__ == '__main__':
    bot.polling()
    while True:
        pass