#!/bin/bash
set -m

uwsgi --ini /usr/src/app/uwsgi.ini & nginx -c /etc/nginx/nginx.conf