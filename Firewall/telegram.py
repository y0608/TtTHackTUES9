import os
import telebot

def func(IP):
    API_KEY = '5819705483:AAES2EIQlIfmyU8GT1jv2GnK07R-p4gOv6A'
    bot = telebot.TeleBot(API_KEY)
    message = IP + " has been banned"
    chat_id = -1001935927840
    bot.send_message(chat_id=chat_id, text=message)



