#!/bin/bash

# Install HomeScript Automations
# v1.0

if [ "$(uname -s)" == "Darwin" ]; then
    echo "HomeScript Automations cannot install on MacOS. Consider installing on Linux."
else
    PRESENT=$(sudo grep cron.hs /etc/crontab)
    if [ "$PRESENT" == "" ]; then
        mkdir ~/cron.hs
        sudo echo "* * * * * $USER cd ~ && run-parts --report ~/cron.hs" >> /etc/crontab
        echo "Done."
    else
        echo "HomeScript Automations already installed."
    fi
fi
