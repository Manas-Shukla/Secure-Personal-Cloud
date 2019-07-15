import server
import client
import argparse

'''
    the following script is the root to all commands
    according to commands given in through command line
    it calls functions imported from server and client
'''

#custom ArgumentParser
class MyArgumentParser(argparse.ArgumentParser):
    def _check_value(self,action,value):
        if action.choices is not None and value not in action.choices:
            raise MyArgumentParser.error(self,'Invalid')
    def error(self,message):
        print('Error: ',message)
        self.exit(2)

#input validation afterwards
parser = MyArgumentParser()

# add add_mutually_exclusive_group to allow one at a time access
g = parser.add_mutually_exclusive_group()
g.add_argument('--server',type=str,nargs='+',help='used for customising server')
g.add_argument('--client',type=str,help = 'used for customising client')
g.add_argument('--about',type=str,choices=['help','version'],help = "following options are supported 'help','version'")


args = parser.parse_args()

if args.server is not None:
    # call server with the given parameters
    server.process(args.server)

elif args.client is not None:
    # call client with the given parameters
    client.process(args.client)

elif args.about is not None:
    if args.about == 'help':
        print('----pending----')
    else :
        print('''####################
spc (GNU coreutils) 1.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Manas Shukla.
####################''')
else:
    print("#type spc help to get list of all possible commands#")
