#!/bin/bash

# Uninstall HomeScript Automations
# v1.0

if [ "$(uname -s)" == "Darwin" ]; then
    echo "HomeScript Automations cannot install on MacOS. Consider installing on Linux."
else
    PRESENT=$(sudo grep cron.hs /etc/crontab)
    if [ "$PRESENT" <> "" ]; then
        sudo grep -v cron.hs /etc/crontab > /etc/cron2 && sudo mv /etc/cron2 /etc/crontab
        echo "HomeScript Automations uninstalled. You may manually delete your automations from ~/cron.hs"
    else
        echo "HomeScript Automations is not installed."
    fi
fi
