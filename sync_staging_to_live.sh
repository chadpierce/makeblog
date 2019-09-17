#!/bin/sh
echo "copying ~/staging directory to /var/www/html live webroot"
rsync -avz --delete staging/* /var/www/html
echo "donezo"
