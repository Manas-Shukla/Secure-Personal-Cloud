#!/bin/bash

if [[ $# -eq 0 ]];then
   echo "missing path name"
   exit
fi

echo "copying files to path"

dir=`realpath $1`
cp -R ./linux_client "$dir"
var=$dir/linux_client/spc.sh

echo "creating aliases"

echo alias spc="'""bash "$var"""'" | cat >> $HOME/.bashrc
# echo "sync_file()"| cat >> $HOME/.bashrc
# echo "{"| cat >> $HOME/.bashrc
# echo "     spc client login"| cat >> $HOME/.bashrc
# echo "     spc sync"|cat >> $HOME/.bashrc
# echo "}"| cat >> $HOME/.bashrc
# echo "export -f sync_file"|cat >> $HOME/.bashrc

source ~/.bashrc

echo "creating man page"
sudo cp ./linux_client/spc_man /usr/local/man/man1/spc.1
sudo gzip /usr/local/man/man1/spc.1

echo "creating backup services"
script=$dir/linux_client/script.sh
save_at=$dir/linux_client/job.cron
echo  "* * * * * bash "$script"" |cat > "$save_at"

crontab "$save_at"


