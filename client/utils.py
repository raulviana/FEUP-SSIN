import symmetric_encryption 

SERVER_ADDRESS = "http://127.0.0.1:3000"
SERVER_PORT = 3000
LOCALHOST = "127.0.0.1"
SIZE = 16

class ExceptionNoUsernameFound(Exception):
    pass

class ExceptionUserNotFound(Exception):
    pass

class ExceptionUserNotAvailable(Exception):
    pass

# Return json data with username, cl_token and new_iv, and the other things in the data encrtpted
def prepare_request(config, data):
    
    username = config["USERNAME"]
    curr_token = config["TOKEN"]
    symmetric_key = config["KEY"]
    
    # Encrypt token
    symmetric_key_iv = symmetric_encryption.create_new_iv(SIZE)
    enc_token = symmetric_encryption.encrypt(curr_token, symmetric_key_iv.encode(), symmetric_key.encode())
    
    res = {"username": username, "cl_token":enc_token, "new_iv": symmetric_key_iv}
    
    # Encrypt others
    for i in data.keys():
        res[i] = symmetric_encryption.encrypt(data[i], symmetric_key_iv.encode(), symmetric_key.encode())
    
    return res