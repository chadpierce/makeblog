#!/bin/sh
datestamp=$(date '+%Y-%m-%d_%H%M')
filename="SOMESITE_full_backup_$datestamp"

tar -zcvf "$filename.tar.gz" /home/dahc
echo "[+] backup created: $filename.tar.gz"
