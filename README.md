# FEUP-SSIN

Repository for the [*Segurança em Sistemas Informáticos*](https://sigarra.up.pt/feup/pt/UCURR_GERAL.FICHA_UC_VIEW?pv_ocorrencia_id=459501 "Course Page") course.

## Group Elements

- [Pedro Galvão](https://github.com/pedrogalvao)
- [Eduardo Macedo](https://github.com/EduMacedo99)
- [Ana Rita Santos](https://github.com/artfs)
- Raul Viana

## Tools

Pyhton, Javascript, openssl, sqlite3


--- 

### Install

    $ npm install

### Create Database

    $ cd database
    $ cat create.sql | sqlite3 Database.db
    or (testing)
    $ cd server
    $ python create_table.py

### Create two clients

    To send messages between two clients run them from different folders
    Pre-registration needed on both

    $ cp -r client ./client2

### Pre-registration & Start Server "face-to-face"

    $ cd server
    $ python register_app.py
    $ node index

### First Registration &/or Authentication (New Session)

    $ cd client
    $ python client.py

- Main Menu
  1. Request service
     1. Calculation of square root (security level: 1)
     2. Calculation of cubic root (security level: 2)
     3. Paramaterized n-root (security level: 3)
  2. Send message
  3. Check received messages

## Encrypt Process

### Registration

---

### Client asks for server public key.

### Server Response:

- not encrypted: public_key

---

---

### Client:

- not encrypted: username
- encrypted (rsa): one_time_id, new_iv, symmetric_key, time

### Server Response:

- encrypted(symmetric): token

---

## Authentication

---

### Client Challenge Request:

- not encrypted: username, new_iv
- encrypted(symmetric): token, msg, time

### Server Response:

- not encrypted: challenge, new_iv
- encrypted(symmetric): succ_msg

---

### Client Challenge Solved Request:

- not encrypted: username, new_iv
- encrypted(symmetric): "challenge", time

### Server Response:

- not encrypted: new_iv
- encrypted(symmetric): new_token, succ_msg

---

## Services

---

### Client set ip Request:

- not encrypted: username, new_iv
- encrypted(symmetric): token, ip_port, time

### Server Response:

- not encrypted: new_iv
- encrypted(symmetric): succ_msg

---

---

### Client get ip Request:

- not encrypted: username, new_iv
- encrypted(symmetric): token, username_2, time

### Server Response:

- not encrypted: new_iv, ip_port
- encrypted(symmetric): ip_port, succ_msg

---

---

### Client service Request:

- not encrypted: username, new_iv
- encrypted(symmetric): token, service_data, time

### Server Response:

- not encrypted: new_iv
- encrypted(symmetric): succ_msg with the value

---

---

### Client set public_key Request:

- not encrypted: username, new_iv
- encrypted(symmetric): token, public_key, time

### Server Response:

- not encrypted: new_iv
- encrypted(symmetric): succ_msg

---

---

### Client get public_key Request:

- not encrypted: username, new_iv
- encrypted(symmetric): token, username_2, time

### Server Response:

- not encrypted: new_iv, ip_port
- encrypted(symmetric): public_key, succ_msg

---
