#! /usr/bin/env python3

import random
import string
import config

#db stuff
import sqlite3
with sqlite3.connect('tekweb_helper.db') as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username text PRIMARY KEY,
                    passwd text NOT NULL,
                    id text not null
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS g (
                    num text PRIMARY KEY,
                    id text not null
                );''')

def setInDb(user, pwd, _id):
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("insert or replace into users values (?, ?, ?);", (user, pwd, _id, )) 

def isInDb(user):
    ret = False
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT() FROM users WHERE username = ?;", (user,))
        count = c.fetchone()[0]
        assert(count <= 1)
        ret = count == 1
    return ret

def getFromDb(user):
    ret = ""
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("SELECT passwd FROM users WHERE username = ?;", (user,))
        ret = c.fetchone()[0]
    assert(ret != "")
    return ret

def getIdFromDb(user):
    ret = ""
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?;", (user,))
        ret = c.fetchone()[0]
    assert(ret != "")
    return ret

def getAllFromDb():
    ret = []
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        for row in c.execute("SELECT * FROM users;"):
            ret.append({
                    "username": row[0],
                    "passwd": row[1]
                })
    return ret

def setGroupId(_id):
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("insert or replace into g values (?, ?);", (1, _id, )) 

def getGroupId():
    ret = ""
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM g WHERE num = 1;")
        ret = c.fetchone()[0]
    assert(ret != "")
    return ret

# bot stuff
## roba utile:
##  update.effective_chat.id := identificatore chat, utile dopo
from telegram.ext import *
import telegram

bot = telegram.Bot(token=config.token)
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher
admin="tk_badcoffee"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="bot per tekweb helper")

dispatcher.add_handler(CommandHandler('start', start))

def _set(update, context):
    user = update.effective_user.username
    if user != admin:
        context.bot.send_message(chat_id=update.effective_chat.id, text="cant set" + user)
    else:
        setGroupId(update.effective_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="gruppo settato")

dispatcher.add_handler(CommandHandler('set', _set))

charset = string.ascii_lowercase + string.digits 
def getRandPwd(l = 8):
    out = ""
    for i in range(l):
        out += random.choice(charset)
    return out

def isUserInGroup(username, _id):
    try:
        group_id=getGroupId()
        return bot.get_chat_member(group_id, _id)["user"]["username"] == username
    except:
        return False
        
def pwd(update, context):
    username = update.effective_user.username 
    _id = update.effective_user.id 
    if not isUserInGroup(username, _id):
        context.bot.send_message(chat_id=update.effective_chat.id, text="non sei nel gruppo di tekweb, sry")
        return
    if (isInDb(username) ):
        passwd = getFromDb(username)
    else:
        passwd = getRandPwd()
        setInDb(username, passwd, _id)
    resptext = "il tuo username: {}\nla tua password: {}".format(username, passwd)
    context.bot.send_message(chat_id=update.effective_chat.id, text=resptext)

dispatcher.add_handler(CommandHandler('pwd', pwd))


print(getGroupId())

updater.start_polling()

#files stuff
from os import listdir, mkdir
from os.path import join, isdir

respath = "./res/"

def newProva(data, filepath):
    mkdir(join(respath, data))
    
def listProve():
    obj = [{ 
              "data": f,
              "path": join(respath, f, "prova.pdf"),
              "soluz": [{ 
                        "nome": s, 
                        "path": join(respath, f, s)
                  } for s in listdir(join(respath, f)) if s.endswith(".zip")]
        } for f in listdir(respath) if isdir(join(respath, f))]
    return sorted(obj, key=lambda a : a["data"])

def provaExists(date):
    provelist = [f for f in listdir(respath) if isdir(join(respath, f))]
    return date in provelist

def getSoluzPath(date, username):
    return join(respath, date, username + ".zip")



#bottle stuff
from bottle import *
@route('/')
def index():
    return template('index', userList=getAllFromDb(), proveList=listProve())

@route('/res/<path:path>')
def callback(path):
    return static_file(path, root='/home/yolo/res/')

@post('/upload')
def upload():
    def end(risultato, ok=False):
        return template('''
            <h3 style="color: {{color}}">{{risultato}}</h3>
            <a href="/">torna alla home</a>
        ''', risultato=risultato, color="green" if ok else "red")

    username = request.forms.get('username')
    if not isInDb(username):
        return end("utente {} non in db".format(username))

    passwd = request.forms.get('passwd')
    if passwd != getFromDb(username):
        return end("password errata")

    data = request.forms.get('data')
    if not provaExists(data):
        return end("prova non esistente, contattami se vuoi aggiungerla")

    upload = request.files.get('upload')
    print(upload)
    name, ext = os.path.splitext(upload.filename)
    if ext != ".zip":
        return end("solo zip ammessi")    
    upload.save(getSoluzPath(data, username))
    
    return end("tutto ok", ok=True)

run(host='0.0.0.0', port=8080)
