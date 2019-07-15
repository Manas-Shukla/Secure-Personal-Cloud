from Crypto.Cipher import Blowfish
from Crypto import Random
from struct import pack


def encrypt_bf(file,password,save_as):
    with open(file,"rb") as f:
        msg=f.read()
    bs = Blowfish.block_size
    key=bytes(password,'utf-8')
    iv = Random.new().read(bs)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    plen = bs - divmod(len(msg), bs)[1]
    padding = [plen]*plen
    padding = pack('b'*plen, *padding)
    msg = iv + cipher.encrypt(msg + padding)
    if len(msg) % 8 != 0:
        toAdd = 8 - len(msg) % 8
        for i in range(toAdd):
            msg=msg+"="
    with open (save_as,"wb") as f:
        f.write(msg)
def decrypt_bf(file,password,save_as):
    with open (file, "rb") as f:
        ciphertext=f.read()
    bs = Blowfish.block_size
    iv = ciphertext[:bs]
    #print(ciphertext)
    ciphertext = ciphertext[bs:]
    key = bytes(password, 'utf-8')
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    out = cipher.decrypt(ciphertext)
    last_byte = out[-1]
    out = out[:- (last_byte if type(last_byte) is int else ord(last_byte))]
    with open(save_as,"wb") as f:
        f.write(out)



# bs = Blowfish.block_size
# key= b'1234567890123456'
# iv = Random.new().read(bs)
# cipher= Blowfish.new(key, Blowfish.MODE_CBC, iv)
# plaintext = b'Hello World '
# plen = bs - divmod(len(plaintext),bs)[1]
# padding = [plen]*plen
# padding = pack('b'*plen, *padding)
# msg = iv + cipher.encrypt(plaintext + padding)
# print(msg)
#
#
# #decryption
# ciphertext=msg
# iv=ciphertext[:bs]
# ciphertext=ciphertext[bs:]
#
# cipher = Blowfish.new(key,Blowfish.MODE_CBC,iv)
# out=cipher.decrypt(ciphertext)
#
# last_byte=out[-1]
# out = out[:- (last_byte if type(last_byte) is int else ord(last_byte))]
# print(repr(out))
