import sqlite3
import string
import random
import getpass
from hashlib import sha256
from register_app import create_table, new_user


# def create_table(conn=sqlite3.connect('database/Database.db')):
#     conn.execute('''DROP TABLE IF EXISTS users;''')
#     conn.execute('''
#                  CREATE TABLE USERS (
#                      username CHAR[8] NOT NULL PRIMARY KEY, 
#                      password_hash TEXT,
#                      security_level INT CHECK(3 >= security_level >= 1),
#                      one_time_id TEXT,
#                      ip_address TEXT,
#                      token TEXT,
#                      symmetric_key TEXT,
#                      symmetric_key_iv TEXT,
#                      challenge TEXT,
#                      challenge_timeout DATE
#                  )
#                  ''')


# def new_user(username, password, security_level, one_time_id, connection=sqlite3.connect('database/Database.db')):
#     conn.execute('INSERT INTO users VALUES ("'
#                  + username + '", "'
#                  + sha256(bytes(password, "ascii")).hexdigest() + '", "'
#                  + security_level + '", "'
#                  + sha256(bytes(one_time_id, "ascii")).hexdigest() +
#                  '", null, null, null, null, null, null);')

def generate_id():
    chrs = string.ascii_letters + string.digits
    return ''.join([random.choice(chrs) for i in range(12)])


def print_table(conn):
    r = conn.execute('SELECT * FROM users')
    for row in r:
        print(row)

conn = sqlite3.connect('../database/Database.db')
create_table(conn)
one_time_id = generate_id()
print(one_time_id)
new_user("Pedro", "2", one_time_id, conn)
new_user("User1", "1", one_time_id, conn)
new_user("User2", "2", one_time_id, conn)
new_user("User3", "3", one_time_id, conn)
print_table(conn)

conn.commit()
conn.close()