#!/bin/bash
/etc/init.d/nginx restart
uwsgi --ini ./docker_files/uwsgi.ini
