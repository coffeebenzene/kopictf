#!/usr/bin/env bash

# remember to chmod +x this file.
# Use crontab -e, add
# * * * * * ~/kopihost/monitor.sh >> ~/kopihost/monitor.log
# Use crontab -r to clear crontab.

cd ~/kopihost

for entity in alice bob; do
    if ! pgrep -xf "python3 $entity.py"; then # If process not running
        nohup python3 $entity.py > log_$entity.out 2>&1 & # start it.
        echo "$(date) Restarted $entity.py" >> monitor.log
    fi;
done;