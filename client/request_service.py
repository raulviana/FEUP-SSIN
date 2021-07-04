from Crypto.PublicKey import RSA
import requests
import binascii
from datetime import datetime

import symmetric_encryption
from utils import *

def request_service(config):  
    if config == None:
        raise ExceptionNoUsernameFound
    
    print("\n> Choose the desired service:")
    print("     1 - Square root")
    print("     2 - Cubic root")
    print("     3 - Parametrized n-root")
    
    service_id = input("Service: ")
    radicand = input("Choose the radicand: ")
    
    data = {"service_id": service_id, "radicand":radicand, "time": str(datetime.now())}
    
    if service_id == "3":
        data["index"] = input("Choose Index: ")
    elif service_id != "1" and service_id !="2":
        print("Invalid option:", service_id)
        return
    
    # Request service
    res = requests.get(SERVER_ADDRESS + "/service", 
        json = prepare_request(config, data)
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok or res.status_code == 501: # or dont have permission
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        if res.status_code != 501:
            print("> Service done with success.\n")
        else:
            print("> Service failed.\n")
    else:
        print("> Server: " + res_content["msg"])
        print("> Service failed.\n")


def request_set_ip(config, ip):
    if config == None:
        raise ExceptionNoUsernameFound
    
    # Request to set ip
    res = requests.post(SERVER_ADDRESS + "/service/set_ip",
        json = prepare_request(config, {"ip_address": ip, "time": str(datetime.now())})
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok: 
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        print("> Set IP done with success.\n")
    else:
        print("> Server: " + res_content["msg"])
        raise ExceptionNoUsernameFound

def request_get_ip(config, username_2):
    if config == None or username_2 == None:
        raise ExceptionNoUsernameFound

    # Request ip of username_2
    res = requests.get(SERVER_ADDRESS + "/service/get_ip",
        json = prepare_request(config, {"username_2":username_2, "time": str(datetime.now())}) 
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok: 
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        ip_response= symmetric_encryption.decrypt(res_content["ip_port"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        print("> Get IP with success.\n")
        return  ip_response
    else:
        print("> Server: " + res_content["msg"])
        if res.status_code == 501:
            raise ExceptionUserNotAvailable
        else:
            raise ExceptionUserNotFound


def request_public_key(config, username_2):
    # Request public key of username_2
    res = requests.get(SERVER_ADDRESS + "/service/public_key",
        json =  prepare_request(config, {"username_2":username_2, "time": str(datetime.now())})  
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok: 
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg and public key
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        key_response= symmetric_encryption.decrypt(res_content["public_key"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        print("> Get public key with success.\n")
        # print(key_response)
        # print(binascii.unhexlify(key_response))
        return RSA.importKey(binascii.unhexlify(key_response))
        #return RSA.importKey(key_response)
    else:
        print("> Server: " + res_content["msg"])
        raise ExceptionUserNotFound


def request_set_pub_key(username, key_token):
    with open("public.key", 'rb') as content_file:
        public_key = content_file.read()
    
    config = {"USERNAME":username, "TOKEN":key_token[1], "KEY":key_token[0]}
    # print(public_key)
    # print(str(binascii.hexlify(public_key))[2:-1])
    res = requests.post(SERVER_ADDRESS + "/service/public_key",
        json = prepare_request(config, {"public_key":str(binascii.hexlify(public_key))[2:-1], "time": str(datetime.now())})
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok: 
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        print("> Set Pub Key with success.\n")
    else:
        print("> Server: " + res_content["msg"])
        print("> Error trying to set pub key.\n")