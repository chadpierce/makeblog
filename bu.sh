#!/bin/sh
datestamp=$(date '+%Y-%m-%d_%H%M')
filename="SOMENAME_$datestamp"
backuplog=backup.log

tar -zcvf "$filename.tar.gz" /var/www/html
echo "[+] backup created: $filename.tar.gz"
echo "[-] INPUT REQUIRED!"
echo "    Enter change details if applicable, or leave blank if you want."
read -p "    > " details
if [ -z "$details" ]
then
	details="no details"
	echo "[-] no details added to $backuplog"
else
	echo "[+] details added to $backuplog"
fi
logstring="$datestamp - $details"
echo $logstring >> $backuplog
echo "[+] work complete"
