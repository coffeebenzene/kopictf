#!/usr/bin/env bash

hostdir="$HOME/host"
if [ -n "$1" ];
    then
        $hostdir="$1";
fi;

mkdir -p $hostdir

cp alice.py bob.py cert.py dhke.py keygen.py router_lib.py monitor.sh $hostdir

cd $hostdir
python3 keygen.py
chmod +x monitor.sh
{ crontab -l; echo "* * * * * cd $(pwd) && ./monitor.sh >> monitor.log 2>&1"; } | crontab - ;