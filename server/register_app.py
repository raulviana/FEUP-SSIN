import sqlite3
import string
import random
import getpass
from hashlib import sha256

DATABASE_PATH = '../database/Database.db'

def create_table(conn=sqlite3.connect(DATABASE_PATH)):
    conn.execute('''DROP TABLE IF EXISTS users;''')
    conn.execute('''
                 CREATE TABLE USERS (
                    username CHAR[8] NOT NULL PRIMARY KEY, 
                    security_level INT CHECK(3 >= security_level >= 1) NOT NULL,
                    one_time_id TEXT NOT NULL,
                    ip_address TEXT,
                    public_key TEXT,
                    token TEXT,
                    symmetric_key TEXT,
                    challenge TEXT,
                    challenge_timeout DATE
                 )
                 ''')


def generate_id():
    chrs = string.ascii_letters + string.digits
    return ''.join([random.choice(chrs) for i in range(12)])


def new_user(username, security_level, one_time_id, conn=sqlite3.connect(DATABASE_PATH)):
    conn.execute('INSERT INTO users VALUES ("'
                 + username + '", "'
                 + security_level + '", "'
                 + sha256(bytes(one_time_id, "ascii")).hexdigest() +
                 '", null, null, null, null, null, null);')


def display_table(conn=sqlite3.connect(DATABASE_PATH)):
    cursor = conn.execute('''SELECT * FROM users;''')
    print("Cursor:", cursor)
    for row in cursor:
        print("username = ", row[0])
        print("password_hash = ", row[1])
        print("Security level = ", row[2])
        print("One time Id = ", row[3])
        print("IP = ", row[4])
        print("Public Key = ", row[5])
        print("Token = ", row[6])
        print("Symmetric Key = ", row[7])
        print("Challenge = ", row[8])
        print("Challenge Timeout = ", row[9])
        

if __name__ == "__main__":
    conn = sqlite3.connect(DATABASE_PATH)
    print("\n> Opened database successfully.\n")

    username = input("Please enter collaborator username: \n")

    security_level = input(
        "What is the security clearance level for this client? \n")

    one_time_id = generate_id()

    print("Important! Take note of your ID: ", one_time_id, "\n")

    new_user(username, security_level, one_time_id, conn)
    conn.commit()
    conn.close()

    print("> Register completed.\n")
