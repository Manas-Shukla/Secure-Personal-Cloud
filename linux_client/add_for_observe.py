import json
import os,sys

'''
    this script adds file/dir to observe.js
    json data is dict of dict indexed by abs path name so that client can sync
    individual as well all files/dir according to his/her choice
'''



base_path = sys.path[0]+'/'
try:
    js = json.load(open(base_path+'observe.js'))
except:
    with open(base_path+'observe.js','w') as fh:
        fh.write('{}')
    js = json.load(open(base_path+'observe.js'))


d = dict()


if sys.argv[1]=='1':
    #directory
    d['path'] = sys.argv[2]
    d['type'] = 1

elif sys.argv[1]=='0':
    #ord file
    d['path'] = sys.argv[2]
    d['type'] = 0

if(d!={}):
    js[d['path']] = d
json.dump(js,open(base_path+'observe.js','w'),sort_keys=True,indent=4)
