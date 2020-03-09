#!/bin/sh

nginx
certbot --nginx --non-interactive --agree-tos -m qcarchive@molssi.org -d qcarchive-webapps.eastus.cloudapp.azure.com
