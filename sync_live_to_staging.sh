#!/bin/sh
echo "copying /var/www/html live webroot to ~/staging directory"
rsync -avz --delete /var/www/html/* ~/staging
echo "donezo"
