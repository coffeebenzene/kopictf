#!/usr/bin/env bash

# remember to chmod +x this file.
# Use crontab -e, add
# * * * * * ~/host/monitor.sh >> ~/host/monitor.log
# Use crontab -r to clear crontab.

cd ~/host

for entity in alice bob; do
    if ! pgrep -xf "python3 $entity.py"  > /dev/null; # If process not running
    then
        nohup python3 $entity.py >> log_$entity.out 2>&1 & # start it.
        echo "$(date) Restarted $entity.py" >> monitor.log
    fi;
done;