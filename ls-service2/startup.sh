#!/bin/bash

pm2 set pm2-logrotate:max_size 500m
pm2 set pm2-logrotate:compress true
pm2 save

if [ ! "$BUILD" ]
then

    if [ "$CRON" = "1" ]
    then
        pm2-runtime start ecosystem.config.js --only cron
    fi

    if [ "$PORT" ]
    then
        pm2-runtime start ecosystem.config.js --only app
    fi
fi


