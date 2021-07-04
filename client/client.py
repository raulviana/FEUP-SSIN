#!python3
import os
import os.path
import re
import random
import string
import requests
import base64
import dotenv
import pyAesCrypt
from os import path
from dotenv import load_dotenv, dotenv_values
from getpass import getpass
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from threading import Thread
from datetime import datetime
import atexit

from assymmetric_encryption import save_key_pair
import symmetric_encryption
import auth
from request_service import ExceptionUserNotFound
from messages import listen_socket, send_message
from request_service import request_service, request_set_ip, request_get_ip, request_public_key, request_set_pub_key
from utils import *

SERVER_KEY_PATH = "resources/server_public.pem"
SERVER_URL = "http://127.0.0.1:3000/"
SIZE = 16

keyToDecrypt = ''


saveEnv = []
username =''

# After the session is done or something wrong happens,set the client as not available
def close_client(value=0, config=None):
    if(config != None):
        # Agora ao colocar "NOT_AVAILABLE", o server vai saber que nao está disponivel
        print("> Set client as not available.")
        request_set_ip(new_config, "NOT_AVAILABLE")
        
    exit(value)
   
def registration():
    global username

    print("\n> Start Registration.\n")
    
    counter_pw = 0
    username = input("\nInsert the username you chose on the server registration:\n")
    ID = input('Insert the unique ID you were given in the server registration:\n')

    server_info = server_reg(username, ID)

    if len(server_info) > 0:

        # polos a escolher uma password
        while counter_pw < 3:
            # Ask for strong password
            print('> Insert your a new password for this device. The password should at least:\n\t- Have 8 characters or more\n\t- Include Uppercase letters\n\t- Include numbers')
            save_pw = getpass()

            rexes = ('[A-Z]', '[a-z]', '[0-9]')

            if len(save_pw) >= 8 and all(re.search(r, save_pw) for r in rexes):
                print('\n> Strong password.')
                break
            else:
                print('\n> Password not strong enough... Try again')
                counter_pw += 1
                if counter_pw >= 3:
                    print("> Maximum tries exceeded. Exiting...")     
                    close_client()

        # criar ficheiro .env, por a info, encriptalon e apagá-lo
        f = open(".env", "x")

        # Desencriptar o .aes escrever para lá as variáveis e voltar a encriptá-lo como na autenticação
        try:
            dotenv_file = dotenv.find_dotenv(
                raise_error_if_not_found=True)  # argumento file name existe
        except OSError:
            print('.env not found')

        config = dotenv_values(".env")

        # Colocar info no .env
        dotenv.set_key(dotenv_file, "KEY", saveEnv[0])
        dotenv.set_key(dotenv_file, "TOKEN", saveEnv[1])
        dotenv.set_key(dotenv_file, "USERNAME", username)
        dotenv.set_key(dotenv_file, "ID", ID)

        # encriptá-lo
        pyAesCrypt.encryptFile(".env", ".env.aes", username+save_pw)

        # APAGA MALUCO
        f.close()
        os.remove(".env")

    else:
        print('> Error: Something went wrong')
        close_client(-1)


def server_reg(username, one_time_ID):
    
    print('> Start Registration.')
    
    # prepare encryption variables
    iv =  symmetric_encryption.create_new_iv(SIZE)
    symmetric_key = ''.join(random.choice(string.ascii_lowercase)
                            for x in range(SIZE))

    # First-Registration -> get server public key
    # get server public key
    response = requests.get(SERVER_URL + "register")
    open(SERVER_KEY_PATH, 'wb').write(response.content)

    # encrypt one_time_id, symmetric_key and iv with serverd public  key
    key = RSA.importKey(open(SERVER_KEY_PATH).read())
    cipher = PKCS1_OAEP.new(key)

    one_time_ID_encrypt = base64.b64encode(
        cipher.encrypt(one_time_ID.encode("utf-8")))
    encrypt_key = base64.b64encode(
        cipher.encrypt(symmetric_key.encode("utf-8")))
    encrypt_iv = base64.b64encode(cipher.encrypt(iv.encode('utf-8')))
    encrypt_time = base64.b64encode(cipher.encrypt(str(datetime.now()).encode('utf-8')))
    token_encrypt = requests.post(
        SERVER_URL + "register/get_token",
        json={
            "ID_encrypt": one_time_ID_encrypt.decode(),
            "encrypt_key": encrypt_key.decode(),
            "encrypt_iv": encrypt_iv.decode(),
            "username": username,
            "time": encrypt_time.decode(),
        },
    )
    # print(token_encrypt.status_code)
    if token_encrypt.status_code == 404:
        print('Wrong username')
        return saveEnv
    elif token_encrypt.status_code == 401:
        print('Wrong oneTimeID')
        return saveEnv
    elif token_encrypt.status_code == 500:
        print('Request lifetime expired.')
        return saveEnv
    else:
        token_encrypt = token_encrypt.json()
        # print("encrypted token: " + token_encrypt["token"])
        decrypted_token = symmetric_encryption.decrypt(
            token_encrypt["token"], token_encrypt["new_iv"].encode(), symmetric_key.encode())
        # print("decryptedtoken: " + decrypted_token)
        print("> Server Registration was successfull!\n")
        saveEnv.append(symmetric_key)
        saveEnv.append(decrypted_token)
        return saveEnv

def read_messages():
    global keyToDecrypt

    try:
        pyAesCrypt.decryptFile("log.txt.aes", "log.txt", keyToDecrypt)
    except ValueError:
        print('\n> No messages received yet :(\n')
        return

    f = open("log.txt", "r")
    lines = f.readlines()
    print('\n#################\n')
    for line in lines:
        print(line)
    print('#################\n')
    f.close()

    os.remove('log.txt')
    



def main_menu(my_port, config):
    print("Options:")
    print("1 - Request service")
    print("2 - Send message")
    print("3 - Check received messages")
    print("4 - Exit")
    try:
        option = int(input("option: "))
        if option == 1:
            request_service(config)
        elif option == 2:
            send_message(config)
        elif option == 3:
            read_messages()
        elif option == 4:
            print("> Exiting ...\n")
            return
        else:
            print("Invalid option\n")
    except ValueError:
        print("Invalid option\n")     
    main_menu(my_ip_port, config)

def decrypt_and_read_dotenv():
    global keyToDecrypt
    counter = 0
    while counter < 3:

        # ask for password
        username = input('Username: ')

        password = getpass()

        keyToDecrypt = username+password

        try:
            pyAesCrypt.decryptFile(".env.aes", ".env", keyToDecrypt)
            break
        except ValueError:
            print('\n> Wrong username/password (or file is corrupted).')
            counter += 1
            if counter >= 3:
                print('> Number of tries exceeded. Terminating program...')
                close_client()

    # get info
    try:
        dotenv_file = dotenv.find_dotenv(
            raise_error_if_not_found=True)  # argumento file name existe
    except OSError:
        print('.env not foud')
        close_client()

    config = dotenv_values(".env")


    # delete newly created .env
    os.remove(".env")
    #print(config)
    return config

def user_is_registred():
    # ver se .env.aes existe - se não existir é pq nao houve registo
    return path.exists(".env.aes")

def authentication():
    # Identifying the collaborator locally
    dotenv_config = decrypt_and_read_dotenv()
    
    if (len(dotenv_config) < 2):
        print("> Error: Authentication failed locally.")
        close_client()
      
    # Authenticate with the server and start a new session
    # return ip_port of current session for the client
    return auth.authentication_server(dotenv_config, SERVER_URL, SIZE) 

########################################################### MAIN SCRIPT ###########################################################
        
if user_is_registred() == False:
    registration()
    print('\n> Creating private and public key...')
    save_key_pair()
    print('\n> Update server of your new public key...')
    request_set_pub_key(username, saveEnv)
    proceed = input("Do you want to proceed with login? [y|n]\n")
    if proceed == "n":
        print('> Exiting...\n')
        close_client()     
else:    
    print('\n> Already Registered.')
    
print('> Proceeding with authentication.\n')
#try:
(new_config, my_ip_port) = authentication()
#except:
    #print("> Something went wrong.")
    #close_client(-1)
    

try:
    pyAesCrypt.decryptFile(".env.aes", ".env", keyToDecrypt)
    os.remove(".env.aes")
except ValueError:
    print('\n> .env was corrupted. Exiting...')
    close_client(-1)

try:
    dotenv_file = dotenv.find_dotenv(
        raise_error_if_not_found=True)  # argumento file name existe
except OSError:
    print('.env not found')

dotenv.set_key(dotenv_file, "TOKEN", new_config["TOKEN"])

pyAesCrypt.encryptFile(".env", ".env.aes", keyToDecrypt)

os.remove('.env')

print("> Authentication done.\n")

port = int(my_ip_port.split(":")[1])
listener_thread = Thread(target=listen_socket, args=(new_config, port, keyToDecrypt))
listener_thread.daemon = True
listener_thread.start()
atexit.register(close_client, (0,new_config))

# Services
#print("> client session address: " + my_ip_port)
# agora está a dar o new_config que veio na autenticação e assim nao pede
request_set_ip(new_config, my_ip_port)
main_menu(my_ip_port, new_config)

close_client(config=new_config)

    
