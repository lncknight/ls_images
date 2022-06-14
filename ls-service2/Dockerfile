FROM node:12.14.1-alpine

ENV TIMEZONE=Asia/Hong_Kong

# Create app directory
WORKDIR /usr/src/app

# timezone
RUN apk update && apk add tzdata \
     && cp -r -f /usr/share/zoneinfo/$TIMEZONE /etc/localtime

RUN apk update && apk add bash openssh rsync imagemagick

# RUN npm config set unsafe-perm true

RUN npm -g i pm2 pm2-logrotate

RUN pm2 set pm2-logrotate:max_size 100m \
    && pm2 save

COPY startup.sh /usr/src/app/docker/startup.sh 

COPY ./data /tmp/data
RUN cd /tmp/data \
    && cat x* > tmp.tar.gz \
    && tar xvf tmp.tar.gz \
    && mv GeoLite2-City_20220610/GeoLite2-City.mmdb .. \
    && rm -rf *

EXPOSE 3000

CMD [ "bash", "/usr/src/app/docker/startup.sh" ]
