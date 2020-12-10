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

def rowToUser(row):
    return { "username": row[0], "passwd": row[1], "id": row[2]  }

def setUser(user, pwd, _id):
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("insert or replace into users values (?, ?, ?);", (user, pwd, _id, )) 

def existsUser(user):
    ret = False
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT() FROM users WHERE username = ?;", (user,))
        count = c.fetchone()[0]
        assert(count <= 1)
        ret = count == 1
    return ret


def getUser(user):
    ret = {}
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?;", (user,))
        ret = rowToUser(c.fetchone())
    return ret

def getAllUsers():
    ret = []
    with sqlite3.connect('tekweb_helper.db') as conn:
        c = conn.cursor()
        for row in c.execute("SELECT * FROM users;"):
            ret.append(rowToUser(row))
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
    return ret

