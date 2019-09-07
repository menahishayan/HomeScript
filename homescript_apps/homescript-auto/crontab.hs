# HomeScript Scheduled Automations crontab

SHELL=/bin/bash
HSPATH=

# m h dom mon dow user	command
*   *  * * *    homebridge    cd ~ && run-parts ~/cron.hs
00 12  * * *	homebridge	  
