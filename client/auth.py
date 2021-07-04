from datetime import datetime
import requests
import symmetric_encryption 
import socket

def authentication_server(config, server_ip_url, size):
    """ Authenticate with the server and start a new session 
        Return client ip_port for this session
    """
    
    username = config["USERNAME"]
    curr_token = config["TOKEN"]
    symmetric_key = config["KEY"]
    
    # (prof) em cada sessão, deverão escolher, pode ser o sistema operativo, um porto e comunica-lo ao servidor
    # Set up socket to talk to other clients after authentication, get >>port<<
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 0))
    ip_port = s.getsockname()
    ip_port = str(ip_port[0]) + ":" + str(ip_port[1])
    #print("\n> Client address:", ip_port)
        
    # Encrypt token
    symmetric_key_iv = symmetric_encryption.create_new_iv(size)
    enc_token = symmetric_encryption.encrypt(curr_token, symmetric_key_iv.encode(), symmetric_key.encode())
    enc_time = symmetric_encryption.encrypt(str(datetime.now()), symmetric_key_iv.encode(), symmetric_key.encode())
        
    # Exhange current token with a new token
    res = requests.get(server_ip_url + "auth", 
        json={
            "username": username,
            "cl_token": enc_token,
            "new_iv": symmetric_key_iv,
            "time": enc_time
            } 
    )
    res_content = res.json()
        
    # If server sended challenge
    if res.ok: 
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), symmetric_key.encode())
        print("> Server: " + msg_response)
        
        # Prove you are "username" and solve the challenge N 
        # Encrypt N, and send it back
        symmetric_key_iv = symmetric_encryption.create_new_iv(size)
        enc_challenge = symmetric_encryption.encrypt(res_content["challenge"], symmetric_key_iv.encode(), symmetric_key.encode())
        enc_time = symmetric_encryption.encrypt(str(datetime.now()), symmetric_key_iv.encode(), symmetric_key.encode())
        
        # Send answer
        res = requests.get(server_ip_url + "auth/challengeRefreshToken", 
            json={
                "username": username,
                "enc_challenge": enc_challenge,
                "new_iv": symmetric_key_iv,
                "time": enc_time
            } 
        )
        res_content = res.json()

        # If server sended a new token, means client is authenticated, decrypt the new token and save it
        if res.ok:
            # Get new IV
            iv_response = res_content["new_iv"]
            # Decrypt msg
            msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), symmetric_key.encode())
            print("> Server: " + msg_response)
            # Decrypt token
            curr_token = symmetric_encryption.decrypt(res_content["token"], iv_response.encode(), symmetric_key.encode())
            
            config["TOKEN"] = curr_token;
            print("> Refresh token done.")
            
            return (config, ip_port)

        else:
            print("> Server: " + res_content["msg"])
            print("> Authentication denied.\n")
    else:
        print("> Server: " + res_content["msg"])
        print("> Authentication denied.\n")

