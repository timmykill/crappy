#! /usr/bin/env python3

import random
import string
import config
import dao
import telegram
from telegram.ext import *

bot = telegram.Bot(token=config.token)
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher

usage='''
        Bot di supporto per sito per la condivisione delle soluzioni d'esame
        usage:
            /set [solo admin] -> imposta il gruppo per il controllo degli accessi
            /pwd (consigliabile utilizzare una chat privata con il bot) -> ricevi credenziali per il sito
    '''


def start_help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=usage)

dispatcher.add_handler(CommandHandler('start', start_help))
dispatcher.add_handler(CommandHandler('help', start_help))

def _set(update, context):
    user = update.effective_user.username
    if user != config.admin:
        context.bot.send_message(chat_id=update.effective_chat.id, text="devi essere l'admin per settare il gruppo degli accessi")
    else:
        dao.setGroupId(update.effective_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="gruppo settato")

dispatcher.add_handler(CommandHandler('set', _set))

charset = string.ascii_lowercase + string.digits 
def getRandPwd(l = 8):
    out = ""
    for i in range(l):
        out += random.choice(charset)
    return out

#this doesnt work as it should
def isUserInGroup(username, _id):
    try:
        group_id = dao.getGroupId()
        chatmember = bot.get_chat_member(group_id, _id)
        print(chatmember) #logging while in production
        return True 
    except:
        print("not worked, {}:{}".format(username, _id))
        return True
        
def pwd(update, context):
    username = update.effective_user.username 
    _id = update.effective_user.id 
    if not isUserInGroup(username, _id):
        context.bot.send_message(chat_id=update.effective_chat.id, text="non sei nel gruppo di tekweb, sry")
        return
    if (dao.existsUser(username)):
        passwd = dao.getUser(username)["passwd"]
    else:
        passwd = getRandPwd()
        dao.setUser(username, passwd, _id)
    resptext = "il tuo username: {}\nla tua password: {}".format(username, passwd)
    context.bot.send_message(chat_id=update.effective_chat.id, text=resptext)

dispatcher.add_handler(CommandHandler('pwd', pwd))

updater.start_polling()


