#!/bin/bash
exec_file="/home/pi/github/plantpointNutrients-automation/index.py"
log_dir="/home/pi/github/plantpointNutrients-automation/logs/`date +%F`/"
log_file="`date +%H%M`.log"

eval mkdir -p $log_dir && python3 $exec_file > $log_dir$log_file
