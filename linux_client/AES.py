import base64
from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16

def pad(data):
    length = 16 - (len(data) % 16)
    return data + (chr(length)*length).encode()

def unpad(data):
    return data[:-data[-1]]

def encrypt_AES(file,password,save_as):
    with open (file,"rb") as f:
    	message=f.read()
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(password, AES.MODE_CFB, IV, segment_size=128)
    with open (save_as,"wb") as f:
    	f.write(base64.b64encode(IV + aes.encrypt(pad(message))))

def decrypt_AES(file,password,save_as):
    with open (file,"rb") as f:
    	encrypted=f.read()
    encrypted = base64.b64decode(encrypted)
    IV = encrypted[:BLOCK_SIZE]
    #print(len(IV))
    aes = AES.new(password, AES.MODE_CFB, IV, segment_size=128)
    with open (save_as,"wb") as f:
    	f.write(unpad(aes.decrypt(encrypted[BLOCK_SIZE:])))
