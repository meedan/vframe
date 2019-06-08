#!/bin/bash
set -e
mkdir -p /var/www/check.vframe.io/logs
touch /var/www/check.vframe.io/logs/nginx.access.log
nginx -t
service nginx restart
source activate vframe
npm i && npm run build
conda install -c conda-forge uwsgi
uwsgi --ini nginx/uwsgi.ini