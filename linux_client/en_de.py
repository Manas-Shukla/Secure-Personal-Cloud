import sys
import AES
import pickle
import RSA
import DES
import bf
#base_path = sys.path[0]+'/'
#base_path= '/home/manasshukla/SecurePersonalCloud/linux_client/'

'''
    handles everything related to en-de

'''


def encrypt(file,save_as,schema,base_path):

        if schema=='AES':
            pickle_in = open(base_path+'en-de/aes.p','rb')
            passwd = pickle.load(pickle_in)
            pickle_in.close()
            AES.encrypt_AES(file,passwd,save_as)

        elif schema=='RSA':

            RSA.encrypt_RSA(file,save_as,base_path)

        elif schema=='DES':
            pickle_in = open(base_path+'en-de/des.p','rb')
            passwd = pickle.load(pickle_in)
            pickle_in.close()
            DES.encrypt_DES(file,passwd,save_as)
        elif schema=='BF':
            pickle_in = open(base_path+'en-de/bf.p','rb')
            #print(base_path)
            passwd = pickle.load(pickle_in)
            pickle_in.close()
            bf.encrypt_bf(file,passwd,save_as)

        else :
            print('pending')
            sys.exit(2)


def decrypt(file,save_as,schema,base_path):
        if schema=='AES':
            pickle_in = open(base_path+'en-de/aes.p','rb')
            passwd = pickle.load(pickle_in)
            pickle_in.close()
            AES.decrypt_AES(file,passwd,save_as)
        elif schema=='RSA':
            pickle_in = open(base_path+'en-de/rsa.p','rb')
            code = pickle.load(pickle_in)
            pickle_in.close()
            RSA.decrypt_RSA(file,code,save_as,base_path)
        elif schema=='DES':
            pickle_in = open(base_path+'en-de/des.p','rb')
            passwd = pickle.load(pickle_in)
            pickle_in.close()
            DES.decrypt_DES(file,passwd,save_as)
        elif schema=='BF':
            pickle_in = open(base_path+'en-de/bf.p','rb')
            passwd = pickle.load(pickle_in)
            pickle_in.close()
            bf.decrypt_bf(file,passwd,save_as)
        else :
            print('pending')
            sys.exit(2)






if __name__=='__main__':

    cmd = sys.argv[1]

    if cmd == "list":
        print('#1)RSA')
        print('#2)AES')
        print('#3)DES')

    elif cmd == 'update':
        print('--pending--')

    elif cmd == 'dump':
        print('--pending--')
