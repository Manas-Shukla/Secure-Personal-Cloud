#!/bin/bash


# the following script is the root to all commands
# according to commands given in through command line
# it calls functions imported from server and client



#changes for set up to work
#sed -e 's/base_path = .*/base_path=hallo/g'
#v=`realpath $0`
#base_path = dirname $v
#print(sys.path[0])
v=`realpath $0`
base_path=`dirname $v`
base_path="$base_path"/

case $1 in

    version) echo "####################
spc (GNU coreutils) 1.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Undefined Variables.
####################";;


    help) echo "Following commands are usable :"
        echo "version"
        echo "help"
        echo "server"
        echo "client"
        echo "status"
        echo "observe"
        echo "ignore"
        echo "viewUploads"
        echo "download"
        echo "en-de"
        echo "sync"
        echo "see man page for more details"

    ;;

    server) exec python3 "$base_path"server.py "${@:2}";;

    client) exec python3 "$base_path"client.py "${@:2}";;

    observe) if [[ -d "$2" ]];then
                exec python3 "$base_path"add_for_observe.py 1 "`realpath "$2"`"
            elif [[ -f "$2" ]];then
                exec python3 "$base_path"add_for_observe.py 0 "`realpath "$2"`"
             else
                echo "missing file name type spc help to know more"
             fi;;
    ignore) if [[ $# -gt 1 ]];then
             exec python3 "$base_path"remove_from_observe.py "`realpath $2`"
         else
             exec python3 "$base_path"remove_from_observe.py
         fi;;
    en-de) if [[ $# -gt 1 ]];then
             exec python3 "$base_path"en_de.py $2
         else
             echo "missing arguments ,see man page for more details"
         fi;;
    sync) if [[ $# -gt 1 ]];then
             exec python3 "$base_path"sync.py "`realpath $2`"
         else
             exec python3 "$base_path"sync.py
         fi;;
    #status) cat "$base_path"observe.js;;
    status) exec python3 "$base_path"status.py;;
    viewUploads) exec python3 "$base_path"fetch.py 0;;
    download) exec python3 "$base_path"fetch.py 1 ;;
    lock_out) exec python3 "$base_path"sync.py 2 ;;

esac
