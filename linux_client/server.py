import json
import re
import sys
base_path = sys.path[0]+'/'
'''
    The following file contains code that reads and writes a js object from/to
    server.js that contains info(ip,port) about server
'''

def set_url(url1):
    #validation of url -- remaining
    base_url = url1.strip()

    res = re.findall("http://(.*):([0-9]*)",base_url)

    ip = res[0][0]
    port = res[0][1]
    url = "http://"+ip+':'+port+"/main_server/"

    js = json.load(open(base_path+'server.js'))
    js["ip"] = ip
    js["port"] = port
    js["base_url"] = url
    json.dump(js,open(base_path+'server.js','w'),sort_keys=True,indent=4)


cmd = sys.argv[1:]

if len(cmd)==2 and cmd[0]=='set-url':
    set_url(cmd[1])

if len(cmd)==1 and cmd[0]=='info':
    print(open(base_path+'server.js').read())
else:
    print('Invalid arguments , See man page for details')
