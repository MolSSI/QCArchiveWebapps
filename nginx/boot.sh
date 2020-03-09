#!/bin/sh


certbot --nginx --non-interactive --agree-tos -m qcarchive@molssi.org -d qcarchive-webapps.eastus.cloudapp.azure.com
kill $(ps aux | grep '[n]ginx' | awk '{print $2}')  # certbot can't kill nginx cleanly?
sleep 3
nginx -g "daemon off;"