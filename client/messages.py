
import socket
import os
import pyAesCrypt
from os import path
from datetime import datetime

from assymmetric_encryption import sign_message, check_signature, encrypt_long_message, decrypt_long_message
from request_service import request_public_key, request_get_ip
from utils import *

CIPHER_TEXT_LENGTH = 344


def save_message(message, addr, key):

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if path.exists('log.txt.aes'):
        try:
            pyAesCrypt.decryptFile("log.txt.aes", "log.txt", key)
            os.remove('log.txt.aes')
        except ValueError:
            print('Was not able to decrypt the file')

        f = open("log.txt", "a")
    else:
        f = open("log.txt", "w+")

    sender, message_text = [str(b) for b in message.split(b"\n")[0:2]]
    f.write('Message received' + ' at ' +
            current_time + ' from ' + sender[2:-1] + '\n')
    f.write('> ' + message_text[2:-1])
    f.write('\n')
    f.write('-----------------------------------\n')
    f.close()

    pyAesCrypt.encryptFile("log.txt", "log.txt.aes", key)
    os.remove("log.txt")
    print("Options:")
    print("1 - Request service")
    print("2 - Send message")
    print("3 - Check received messages")
    print("4 - Exit")
    print("option:")


def listen_socket(config, port, key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LOCALHOST, port))
        s.listen()
        print("+ Waiting for messages in port "+str(port))
        while True:
            conn, addr = s.accept()
            print("accept")
            with conn:
                data = conn.recv(CIPHER_TEXT_LENGTH*10)
                message = decrypt_long_message(data)
                if check_signature(config, message):
                    print('\n\n> New Message received from', addr, ' !\n')
                    save_message(message, addr, key)
                else:
                    print('\n\n> Discarding a message with invalid signature !\n')


def send_message(config):
    username_2 = input("Which client do you want to contact?\n")
    try:
        address_and_port = request_get_ip(config, username_2)
        port = int(address_and_port.split(":")[1])
        message = input("Write your message:\n")
        public_key = request_public_key(config, username_2)
        #print("public key")
        # print(public_key)
        complete_message_bytes = bytes(
            config["USERNAME"], "utf-8") + b"\n" + sign_message(bytes(message, "utf-8"))
        encrypted_message = encrypt_long_message(
            complete_message_bytes, public_key)
        # print("1")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #print("with socket")
            s.connect((LOCALHOST, port))
            s.sendall(encrypted_message)
    except ConnectionRefusedError:
        print("> This client is not available at the moment, try again later\n")
    except ExceptionUserNotAvailable:
        print("> This client is not available at the moment, try again later\n")
    except ExceptionUserNotFound:
        print("> This username does not exist in the server database\n")
