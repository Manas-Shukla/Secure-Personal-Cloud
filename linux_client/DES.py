import pyDes


def padd_passwd(password):
	if len(password)<24:
		while len(password)!=24:
			password=password+" "
	else:
		password=password[0:24]
	return password


#binary_stream = io.BytesIO()
#data=""
import base64
def encrypt_DES(file,password,save_as):
	password = padd_passwd(password)
	k=pyDes.triple_des(password, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
	with open(file,'rb') as f:
		#global data
		data = f.read()
		encoded=base64.encodestring(data)

	d=k.encrypt(encoded)
	with open(save_as,'wb') as f:
		f.write(d)


def decrypt_DES(file,password,save_as):
	password = padd_passwd(password)
	k=pyDes.triple_des(password, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
	d = open(file,'rb').read()
	e=k.decrypt(d)
	decoded=base64.decodestring(e)
	with open(save_as,'wb') as f:
		f.write(decoded)
