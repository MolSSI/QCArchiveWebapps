#!/bin/sh

certbot --nginx
nginx -g daemon off;