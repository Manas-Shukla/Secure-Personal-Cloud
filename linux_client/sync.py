import json
import os,sys
import requests
import pickle
import hashlib
import detect_type
import en_de
import re
import signal



'''
    this script syncs file/dir to server whose info is given in server.js
    when given argument it sync only that particular file/directory
    else it will sync all that is observe.js
'''



base_path = sys.path[0]+'/'
schema = open(base_path+'en-de/schema.txt').read().strip()

cjs = json.load(open(base_path+'client.js'))
sjs = json.load(open(base_path+'server.js'))

#bad way but just do it for now
url = sjs['base_url'] + 'file_upload/'
url_lock_in = sjs['base_url'] + 'request_for_sync/'
url_lock_out = sjs['base_url'] + 'request_for_desync/'

username = cjs['username']
password = cjs['password']


def lock_in():
    try:

        pickle_in = open(base_path+'session.p','rb')
        s = pickle.load(pickle_in)
        pickle_in.close()
        res = s.post(url=url_lock_in).text
        pickle_out = open(base_path+'session.p','wb')
        pickle.dump(s,pickle_out)
        pickle_out.close()

        if res.startswith('#FAIL'):
            print(res)
            sys.exit(2)
        if res.startswith('#ACCEPTED'):
            return True
        if res.startswith('#REJECTED'):
            return False



    except:
        print("Please login first!")
        sys.exit(2)



def lock_out():
    try:

        pickle_in = open(base_path+'session.p','rb')
        s = pickle.load(pickle_in)
        pickle_in.close()
        res = s.post(url=url_lock_out).text
        pickle_out = open(base_path+'session.p','wb')
        pickle.dump(s,pickle_out)
        pickle_out.close()

        if res.startswith('#FAIL'):

            print('WARNING : PLease login and release the lock!')
        print(res)





    except:
        print("Please login first!")
        sys.exit(2)


#detect type and all other stuff
def file_to_dict(file):
    d = {}
    tp = detect_type.detect_type(file)
    d['ftype'] = tp[0]
    d['fdesc'] = tp[1]
    d['fname'] = file
    d['fpath'] = file
    d['md5sum'] = hashlib.md5(open(file,'rb').read()).hexdigest()
    return d


#source :: https://stackoverflow.com/questions/9816816/get-absolute-paths-of-all-files-in-a-directory
def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))



def sync_file(file):
    #file is file abs path
    data = file_to_dict(file)

    if True:
        en_de.encrypt(file,base_path+'tmp.aes',schema,base_path)
        orig_md5 = hashlib.md5(open(base_path+'tmp.aes','rb').read()).hexdigest()
        files = {'file':open(base_path+'tmp.aes','rb')}

    else:
        print('''Failed : File not found in its added location
                    Maybe its deleted''')
        return

    try:
        pickle_in = open(base_path+'session.p','rb')
        s = pickle.load(pickle_in)
        pickle_in.close()
        res = s.post(url=url,files=files,data=data).text
        os.remove(base_path+'tmp.aes')
        pickle_out = open(base_path+'session.p','wb')
        pickle.dump(s,pickle_out)
        pickle_out.close()
        try:

            ret_md5 = re.findall('<(.*)>',res)[0]
            if ret_md5==orig_md5:
                print(res)
                print('md5sum--ok')
            else :
                print(res)
                print('md5sum--NOT OK')
        except:
            print(res)


    except:

        #more error handling required
        print("Please login first!")
        sys.exit(2)




def sync_dir(dir):
    #dir is file abs path
    for file in absoluteFilePaths(dir):
        sync_file(file)


def handler(signum, frame):
    print('Sync Interuppted in between')
    print('locking out database----')
    lock_out()
    sys.exit(2)

signal.signal(signal.SIGINT, handler)


try:
    js = json.load(open(base_path+'observe.js'))
except :
    print('Error: observe.js not found')
    sys.exit(2)

#lock_in
ask =lock_in()
if ask==False:
    print('Sync Failed ,It seems some other machine is syncing ,Please try later')
    sys.exit(2)


if len(sys.argv)==1:
    # sync all
    for k,v in js.items():
        if v['type'] == 1:
            sync_dir(v['path'])
        else:
            sync_file(v['path'])
    js = {}
    json.dump(js,open(base_path+'observe.js','w'),sort_keys=True,indent=4)

else:
    #sync single
    p = sys.argv[1]
    if p == '2':
        lock_out()
        sys.exit(2)
    if p in js:
        if js[p]['type'] == 1:
            sync_dir(p)
        else:
            sync_file(p)
        js.pop(p, None)
        json.dump(js,open(base_path+'observe.js','w'),sort_keys=True,indent=4)

    else:
        print('ERROR : File is not yet added to observed mode')

lock_out()
