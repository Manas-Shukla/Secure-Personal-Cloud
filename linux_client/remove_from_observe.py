import json
import os,sys

'''
    this script removes file/dir from observe.js
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
    sys.exit(2)


if len(sys.argv)==1:
    # remove all
    js = {}
    json.dump(js,open(base_path+'observe.js','w'),sort_keys=True,indent=4)

else:
    #remove single
    p = sys.argv[1]
    js.pop(p, None)
    json.dump(js,open(base_path+'observe.js','w'),sort_keys=True,indent=4)
