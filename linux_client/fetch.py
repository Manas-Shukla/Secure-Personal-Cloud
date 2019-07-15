import sys,json,os
import requests,pickle
from termcolor import colored
import en_de
import hashlib

base_path = sys.path[0]+'/'
schema = open(base_path+'en-de/schema.txt').read().strip()


cjs = json.load(open(base_path+'client.js'))
sjs = json.load(open(base_path+'server.js'))

#bad way but just do it for now

username = cjs['username']
password = cjs['password']


def print_tree(T,indent):
    if T == "None" :
        return
    for k,v in sorted(T.items()):
        res = colored(k,'blue') if v != "None" else colored(k,'green')
        print(colored('|---'*indent,'red') + res)
        print_tree(v,indent+1)


def viewUploads():

    url = sjs["base_url"] + 'file_view'
    try:
        pickle_in = open(base_path+'session.p','rb')
        s = pickle.load(pickle_in)
        pickle_in.close()
        res = s.post(url=url).json()
        pickle_out = open(base_path+'session.p','wb')
        pickle.dump(s,pickle_out)
        pickle_out.close()
        return res
    except:


        print("#FAIL:Not Logged In")
        sys.exit()

def download(fpath,save_at):
    if not save_at.endswith('/'):
        save_at += '/'



    url = sjs['base_url'] + 'file_download/'
    data = {'fpath':fpath}
    if True:
        pickle_in = open(base_path+'session.p','rb')
        s = pickle.load(pickle_in)
        pickle_in.close()
        res = s.post(url=url,data=data).content
        pickle_out = open(base_path+'session.p','wb')
        pickle.dump(s,pickle_out)
        pickle_out.close()

        if False and res.startswith('#FAIL'):
            print('Not logged in')
            return None
        else:
            #print(res)
            file_name = fpath.split('/')[-1]



            open(base_path+'tmp.aes','wb').write(res)
            #
            en_de.decrypt(base_path+'tmp.aes',save_at+file_name,schema,base_path)
            os.remove(base_path+'tmp.aes')




    else:
        return "#FAIL:Not Logged In"





if sys.argv[1]=='0':
    res = viewUploads()
    #print(res)
    if isinstance(res,str) and res.startswith('#FAIL'):
        print(res)
    else:
        #print_tree(json.loads(res.replace("\'","\"")),0)
        #print(res.replace("\'","\"").replace('""','"root"'))
        #print_tree(res,0)
        res= res.replace('\0', '').replace("\'","\"")
        print_tree(json.loads(res),0)


else:
    x = input('Enter the path you want to download : ')
    y = input('Where to download? : ')
    #x = '/home/manasshukla/identity.jpeg'
    #y = '/home/manasshukla/Dropbox/'

    download(x,y)
