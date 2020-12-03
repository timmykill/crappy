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
    return static_file(path, root='/root/crappy/res/')

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

run(host='0.0.0.0', port=80, server="tornado")
