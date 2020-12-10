#! /usr/bin/env python3

import random
import string
import config
import dao

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
    return template('index', userList=dao.getAllUsers(), proveList=listProve(), nomeEsame=config.nomeEsame)

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
    if not dao.existsUser(username):
        return end("utente {} non in db".format(username))

    passwd = request.forms.get('passwd')
    if passwd != dao.getUser(username)["passwd"]:
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

run(host='0.0.0.0', port=int(config.port), server="tornado")
