from Crypto import Signature
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64
from os import path

from request_service import request_public_key
from utils import *

CIPHER_TEXT_LENGTH = 344


def save_key_pair():
    key = RSA.generate(2048)
    with open("private.key", 'w+b') as content_file:
        #chmod("private.key", 600)
        content_file.write(key.exportKey('PEM'))
    public_key = key.publickey()
    with open("public.key", 'w+b') as content_file:
        content_file.write(public_key.exportKey('OpenSSH'))


def encrypt_message(message_bytes, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = base64.b64encode(
        cipher.encrypt(message_bytes))
    return encrypted_message

def decrypt_message(message_bytes):
    with open("private.key", 'rb') as content_file:
        private_key = RSA.importKey(content_file.read())
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(base64.b64decode(message_bytes))
    return decrypted_message

def encrypt_long_message(message_bytes, public_key):
    splitted_message = [message_bytes[i:i+128] for i in range(0, len(message_bytes), 128)]
    encrypted_message = b""
    for part in splitted_message:
        encrypted_message += encrypt_message(part, public_key)
    return encrypted_message

def decrypt_long_message(message_bytes):
    splitted_message = [message_bytes[i:i+CIPHER_TEXT_LENGTH] for i in range(0, len(message_bytes), CIPHER_TEXT_LENGTH)]
    decrypted_message = b""
    for part in splitted_message:
        try:
            decrypted_message += decrypt_message(part)
        except:
            print("error decrypting")
    return decrypted_message

def sign_message(message):
    with open("private.key", 'rb') as content_file:
        private_key = RSA.importKey(content_file.read())
    hash = SHA.new(message)
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(hash)
    return message + b"\n" + signature

def check_signature(config, complete_message):
    message_parts = complete_message.split("\n".encode('utf-8'))
    sender, message_text = message_parts[0:2]
    signature = b'\n'.join(message_parts[2:])
    public_key = request_public_key(config, sender.decode('utf-8'))
    verifier = PKCS1_v1_5.new(public_key)
    hash = SHA.new(message_text)
    verified = verifier.verify(hash, signature)
    return verified