#!/bin/sh

certbot --nginx --non-interactive --agree-tos -m qcarchive@molssi.org
nginx -g "daemon off;"