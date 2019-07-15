import base64
from Crypto import Random
from Crypto.Cipher import AES

# fsz = os.path.getsize(infile)
# with open(encfile, 'w') as fout:
#     fout.write(struct.pack('<Q', fsz))
# 	fout.write(iv)
# 	sz = 2048
# 	with open(infile) as fin:
# 		while True:
# 			data = fin.read(sz)
# 			n = len(data)
# 			if n == 0:
# 				break
# 			elif n % 16 != 0:
# 				data += ' ' * (16 - n % 16) # <- padded with spaces
# 			encd = aes.encrypt(data)
# 			fout.write(encd)



BLOCK_SIZE = 16

def pad(data):
    length = 16 - (len(data) % 16)
    return data + (chr(length)*length).encode()

def unpad(data):
    return data[:-data[-1]]

def encrypt(message, passphrase):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(passphrase, AES.MODE_CFB, IV, segment_size=128)
    with open ("enc.bin","wb") as f:
    	f.write(base64.b64encode(IV + aes.encrypt(pad(message))))
   # return (IV + aes.encrypt(pad(message)))

def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    IV = encrypted[:BLOCK_SIZE]
    #print(len(IV))
    aes = AES.new(passphrase, AES.MODE_CFB, IV, segment_size=128)
    with open ("out.jpeg","wb") as f:
    	f.write(unpad(aes.decrypt(encrypted[BLOCK_SIZE:])))

with open ("pp.jpeg", "rb") as f:
	data=f.read()
	#print(data)
	#encoded=base64.encodestring(data)
encrypt(data, "1234567890123456")

with open ("enc.bin","rb") as f:
	decode=f.read()

decrypt(decode, "1234567890123456")


# from Crypto.Cipher import AES

# key = '0123456789abcdef'
# IV = 16 * '\x00'           # Initialization vector: discussed later
# mode = AES.MODE_CBC
# encryptor = AES.new(key, mode, IV=IV)

# text = 'j' * 64 + 'i' * 128
# ciphertext = encryptor.encrypt(text)