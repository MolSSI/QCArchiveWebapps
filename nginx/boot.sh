#!/bin/sh


certbot --nginx --non-interactive --agree-tos -m qcarchive@molssi.org -d qcarchive-webapps.eastus.cloudapp.azure.com
nginx -g "daemon off;"