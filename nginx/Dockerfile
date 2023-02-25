FROM nginx:1.23.1-alpine

ENV ENV prod

RUN apk update && apk add bash inotify-tools supervisor

# timezone
RUN apk add tzdata \
     && cp -r -f /usr/share/zoneinfo/Asia/Hong_Kong /etc/localtime

RUN apk add certbot certbot-nginx

ADD start.sh .

# nginx -g 'daemon off;'
