import json,os,sys,hashlib
import pickle
import hashlib
import requests
import pprint
from termcolor import colored

#pprint.pprint(dict)
pretty_dict_str = pprint.pformat(dict)

def print_nicely(dct):
    #print("Items held:")
    for item in dct:
        print("{} ({})".format(item, dct[item]['']))

base_path = sys.path[0]+'/'

cjs = json.load(open(base_path+'client.js'))
sjs = json.load(open(base_path+'server.js'))

#bad way but just do it for now
# print a-b , a+b, and aintersectionb.
username = cjs['username']
password = cjs['password']


def get_all_files_on_server():

    url = sjs["base_url"] + 'get_md5'
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


def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

observe_set=set([])

def get_all_files_on_observe():
    json_data=open(base_path+'observe.js').read()
    data=json.loads(json_data)
    for key in data:
        if os.path.isfile(key):
            md5hash=hashlib.md5(open(key,'rb').read()).hexdigest()
            observe_set.add((key,md5hash))
        elif os.path.isdir(key):
            for file in absoluteFilePaths(key):
                md5hash=hashlib.md5(open(file,'rb').read()).hexdigest()
                observe_set.add((file,md5hash))
#print(set(get_all_files_on_server().items()))

# to print A
server_set=set(get_all_files_on_server().items())
print(colored("Files on Server:",'red'))
for ele in server_set:
    print(colored(ele[0],'blue'),colored( "  (" + ele[1] + ")",'green'))


get_all_files_on_observe()

print(colored("\nFiles on Observe:",'red'))

for ele in observe_set:
    print(colored(ele[0], 'blue'), colored("  (" + ele[1] + ")", 'green'))

print(colored("\nFiles on Server intersection Observe:",'red'))

intersection=observe_set.intersection(server_set)

for ele in intersection:
    print(colored(ele[0], 'blue'), colored("  (" + ele[1] + ")", 'green'))

print(colored("\nFiles on Server - Observe:",'red'))


for ele in server_set-observe_set:
    print(colored(ele[0], 'blue'), colored("  (" + ele[1] + ")", 'green'))
print(colored("\nFiles on Observe - Server:",'red'))

for ele in observe_set-server_set:
    print(colored(ele[0], 'blue'), colored("  (" + ele[1] + ")", 'green'))
