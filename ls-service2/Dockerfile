FROM node:12.14.1-alpine

ENV TIMEZONE=Asia/Hong_Kong

# Create app directory
WORKDIR /usr/src/app

# timezone
RUN apk update && apk add tzdata \
     && cp -r -f /usr/share/zoneinfo/$TIMEZONE /etc/localtime

RUN apk update && apk add bash openssh rsync imagemagick

RUN npm config set unsafe-perm true

RUN npm -g i pm2 pm2-logrotate

RUN pm2 set pm2-logrotate:max_size 100m \
    && pm2 save

COPY data/GeoLite2-City.mmdb /tmp/GeoLite2-City.mmdb
COPY startup.sh /usr/src/app/docker/startup.sh 

EXPOSE 3000

CMD [ "bash", "/usr/src/app/docker/startup.sh" ]
