import json
import requests
import getpass
import sys
import pickle


base_path = sys.path[0]+'/'

'''
    The following file contains code that reads and writes a js object from/to
    client.js that contains info(username,password) about client
    Also it will be used for sign_up and reseting the password

'''

def sign_up():
    #get url for server.js
    sjs = json.load(open(base_path+'server.js'))
    url = sjs["base_url"] + "sign_up/"
    data = dict()
    cnt = 0
    while True:
        cnt += 1
        if cnt==3:
            print("Try Limit exceeded try again later")
            break

        username = input("Username: ")
        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm Password: ")

#break after maxx
        while confirm != password :
            print("Password not confirmed try again")
            confirm = getpass.getpass("Confirm Password: ")

        data['username'] = username
        data['password'] = password


        try:
            res = requests.post(url=url,data=data).text
        except:
            print("No connection try again later")
            break

        if(res.startswith("#FAIL")):
            print(res)
        else:
            print(res)
            cjs = json.load(open(base_path+'client.js'))
            cjs["username"] = username
            cjs["password"] = password
            json.dump(cjs,open(base_path+'client.js','w'),sort_keys=True,indent=4)
            break

def reset_password():
    #get url for server.js
    sjs = json.load(open(base_path+'server.js'))
    url = sjs["base_url"] + "reset_password" + "/"
    data = dict()
    cnt = 0
    cjs = json.load(open(base_path+'client.js'))

    while True:
        cnt += 1
        if cnt==3:
            print("Try Limit exceeded try again later")
            break

        new_password = getpass.getpass("new Password: ")
        confirm = getpass.getpass("Confirm new Password: ")
        while new_password != confirm:
            print("Password not confirmed try again")
            confirm = getpass.getpass("Confirm new Password: ")
        data['username'] = cjs['username']
        data['old_password'] = cjs['password']
        data['new_password'] = confirm


        try:
            res = requests.post(url=url,data=data).text
        except:
            print("No connection try again later")
            break

        if(res.startswith("#FAIL")):
            print(res)
        else:
            print(res)
            cjs['password'] = confirm
            json.dump(cjs,open(base_path+'client.js','w'),sort_keys=True,indent=4)
            break

def login():
    #get url for server.js
    sjs = json.load(open(base_path+'server.js'))
    url = sjs["base_url"] + "login" + "/"
    data = dict()

    cjs = json.load(open(base_path+'client.js'))

    data['username'] = cjs['username']
    data['password'] = cjs['password']

    try:
        s = requests.session()
        res = s.post(url=url,data=data).text
        pickle_out = open(base_path+'session.p','wb')
        pickle.dump(s,pickle_out)
        pickle_out.close()
        print(res)
    except:
        print("No connection try again later")
        return

def logout():
    sjs = json.load(open(base_path+'server.js'))
    url = sjs["base_url"] + "logout" + "/"
    try:
        pickle_in = open(base_path+'session.p','rb')
        s = pickle.load(pickle_in)
        pickle_in.close()
        res = s.post(url=url).text

    except:
        res = "#Succesfully logged out#"
        pass
    print(res)


def edit():
    cjs = json.load(open(base_path+'client.js','r'))
    cjs['username'] = input('Enter Username: ')
    password = getpass.getpass("Enter Password: ")
    cpassword = None
    while cpassword != password:
        cpassword = getpass.getpass("Confirm Password: ")
    cjs['password'] = password
    json.dump(cjs,open(base_path+'client.js','w'),sort_keys=True,indent=4)


cmd = sys.argv[1:]

if cmd==['info']:
    #print info
    print(open(base_path+'client.js').read())


elif cmd==['sign_up']:
    sign_up()

elif cmd==['reset_password']:
    reset_password()
elif cmd ==['login']:
    login()
elif cmd ==['logout']:
    logout()
elif cmd == ['edit']:
    edit()

else :
    print('Invalid arguments ,See man page for more details')
