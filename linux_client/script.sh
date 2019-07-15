#!/bin/bash

export DISPLAY=:0

v=`realpath $0`
base_path=`dirname $v`
base_path="$base_path"/
#echo $base_path

notify-send 'Syncing files begin'

source ~/spc_env/bin/activate
source ~/.bashrc

python3 "$base_path"client.py login
python3 "$base_path"sync.py
python3 "$base_path"sync.py 2



notify-send 'Syncing finished'
