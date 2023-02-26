#!/bin/bash

# this script not benn run

# htpasswd -b -c /etc/nginx/arena.passwd $ARENA_USER $ARENA_PASSWD
# htpasswd -b -c /etc/nginx/redis_admin.passwd $REDIS_ADMIN_USER $REDIS_ADMIN_PASSWD

# nginx # nginx -g "daemon off;"
# echo 'starting NGINX'
# nginx

# supervisord -c /etc/supervisord.conf

chown -R nginx:nginx /var/log/nginx

echo 'starting NGINX'
nginx -g "daemon off;"
