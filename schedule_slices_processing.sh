#!/bin/sh

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "01 * * * * $(pwd)/trigger_slices_processing.py run >> $(pwd)/slices_processing.log" >> mycron

#install new cron file
crontab mycron
rm mycron