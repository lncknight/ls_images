# Docker template from https://gitlab.com/ric_harvey/nginx-php-fpm
# FROM microsoft/mssql-tools as mssql


# docker pull php:7.4.30-fpm-alpine3.15
FROM surnet/alpine-wkhtmltopdf:3.10-0.12.5-full as wkhtmltopdf
# FROM test as wkhtmltopdf
# FROM surnet/alpine-wkhtmltopdf:3.9-0.12.5-full as wkhtmltopdf

# iconv issue
# FROM php:7.4.30-fpm-alpine3.16
# worked
FROM php:7.3-fpm-alpine3.13

# nginx error
# FROM richarvey/nginx-php-fpm:1.10.4
# FROM richarvey/nginx-php-fpm:1.9.1
# worked
# FROM richarvey/nginx-php-fpm:1.8.2 

LABEL maintainer="Lawrence Lau <lncknight@gmail.com>"

# COPY --from=mssql /opt/microsoft/ /opt/microsoft/
# COPY --from=mssql /opt/mssql-tools/ /opt/mssql-tools/
# COPY --from=mssql /usr/lib/libmsodbcsql-13.so /usr/lib/libmsodbcsql-13.so

# mssql / sql_srv
# https://github.com/coopTilleuls/php-mssql-alpine/blob/master/7.2/cli/Dockerfile
# https://github.com/kohlschutter/junixsocket/issues/33
# support: https://docs.microsoft.com/en-us/sql/connect/php/system-requirements-for-the-php-sql-driver?redirectedfrom=MSDN&view=sql-server-2017
RUN set -xe \
    && apk add --no-cache --virtual .persistent-deps \
        libstdc++ \
        freetds \
        unixodbc \
    && apk add --no-cache --virtual .build-deps \
        $PHPIZE_DEPS \
        unixodbc-dev \
        freetds-dev \
    && docker-php-source extract \
    # && docker-php-ext-install pdo_dblib \
    # && pecl install \
    #     sqlsrv \
    #     pdo_sqlsrv \
    # && docker-php-ext-enable --ini-name 30-sqlsrv.ini sqlsrv \
    # && docker-php-ext-enable --ini-name 35-pdo_sqlsrv.ini pdo_sqlsrv \
    && docker-php-source delete \
    && apk del .build-deps


# resolves #166
ENV LD_PRELOAD /usr/lib/preloadable_libiconv.so php
RUN apk add --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community gnu-libiconv


# alpine repo
# https://stackoverflow.com/questions/49067625/how-can-i-use-chinese-in-alpine-headless-chrome
# https://blog.csdn.net/zimou5581/article/details/101368129
RUN echo @edge http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories


ENV TIMEZONE=Asia/Hong_Kong
RUN apk update && apk add tzdata \
     && cp -r -f /usr/share/zoneinfo/$TIMEZONE /etc/localtime


RUN apk upgrade --update
# RUN apk update

# basic
# RUN buildDeps=" \
#     # linux-headers \
#     # autoconf \
#     # g++ \
#     # gcc \
#     # libc-dev \
#     # make \
#     " \
#     runtimeDeps=" \
#         git \
#         nodejs \
#         npm \
#         nginx \
#         rsync \
#     "

# RUN apk add $buildDeps $runtimeDeps && apk del $buildDeps
# RUN apk add $runtimeDeps

# base
RUN apk add --no-cache \
    bash \
    openssh-client \
    wget \
    supervisor \
    curl \
    libcurl \
    libzip-dev \
    bzip2-dev \
    imap-dev \
    openssl-dev \
    git \
    augeas-dev \
    libressl-dev \
    ca-certificates \
    dialog \
    autoconf \
    make \
    gcc \
    musl-dev \
    linux-headers \
    libmcrypt-dev \
    libpng-dev \
    icu-dev \
    libpq \
    libxslt-dev \
    libffi-dev \
    freetype-dev \
    sqlite-dev \
    libjpeg-turbo-dev \
    postgresql-dev
    
# more base

RUN apk add --no-cache imagemagick \
    nodejs \
    npm \
    nginx \
    rsync \
    mysql-client


# php: gd
# ref: https://github.com/docker-library/php/issues/931#issuecomment-568658449
# ref: https://github.com/docker-library/php/issues/912#issuecomment-559918036
RUN docker-php-ext-configure gd --with-freetype-dir=/usr --with-jpeg-dir=/usr --with-png-dir=/usr


# php extensions
RUN docker-php-ext-install iconv pdo_mysql pdo_sqlite pgsql pdo_pgsql mysqli gd exif intl xsl json soap dom zip opcache

RUN pecl install -o -f redis && \
    echo "extension=redis.so" > /usr/local/etc/php/conf.d/redis.ini && \
    docker-php-source delete

# misc    
RUN apk update && apk add python3 \
    && wget  https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py

RUN mkdir -p /etc/nginx && \
    mkdir -p /var/www/app && \
    mkdir -p /run/nginx && \
    mkdir -p /var/log/supervisor && \
    pip install -U pip && \
    apk del gcc musl-dev linux-headers libffi-dev augeas-dev make autoconf
    
    
# swoole
# ref: https://github.com/swoole/swoole-src/issues/1557
# issue: https://askubuntu.com/questions/509663/c-preprocessor-lib-cpp-fails-sanity-check/509671
# RUN apk add --no-cache --virtual .build-deps \
#     linux-headers \
#     autoconf \
#     g++ \
#     gcc \
#     libc-dev \
#     make \
#     git \
#     && git clone https://github.com/swoole/swoole-src.git \
#     && ( \
#         cd swoole-src \
#         && phpize \
#         && ./configure --enable-swoole-debug --enable-mysqlnd \
#         && make -j$(nproc) && make install \
#         ) \
#     && rm -r ./swoole-src \
#     && docker-php-ext-enable swoole \
#     && apk del .build-deps \
#     && rm -rf /var/cache/apk/*


# Install dependencies for wkhtmltopdf
# fix ref: https://github.com/anaynayak/aws-security-viz/commit/32930c8d4a6445ff89af1b2af9b85511dade0356
RUN apk add --no-cache \
  libstdc++ \
  libx11 \
  libxrender \
  libxext \
  libssl1.1 \
  ca-certificates \
  fontconfig \
  freetype \
  ttf-dejavu \
  ttf-droid \
  ttf-freefont \
  ttf-liberation \
  ttf-freefont \
  libpng \
  font-adobe-100dpi \
  libjpeg \
  openssl \
  icu \
  font-xfree86-type1 \
  && apk add --no-cache --virtual .build-deps \
  msttcorefonts-installer \
\
# Install microsoft fonts
&& update-ms-fonts \
&& fc-cache -f \
\
# Clean up when done
&& rm -rf /tmp/* \
&& apk del .build-deps


# https://hub.docker.com/r/surnet/alpine-wkhtmltopdf
# Copy wkhtmltopdf files from docker-wkhtmltopdf image
COPY --from=wkhtmltopdf /bin/wkhtmltopdf /bin/wkhtmltopdf
COPY --from=wkhtmltopdf /bin/wkhtmltoimage /bin/wkhtmltoimage
COPY --from=wkhtmltopdf /bin/libwkhtmltox* /bin/
RUN mkdir -p /opt/wkhtmltox/bin/ \
    && ln -s /bin/wkhtmltoimage /opt/wkhtmltox/bin/wkhtmltoimage \
    && ln -s /bin/wkhtmltopdf /opt/wkhtmltox/bin/wkhtmltopdf


# Nodejs
RUN npm config set unsafe-perm true \
    && npm -g i pm2 wscat http-server


# Install Composer.
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && ln -s $(composer config --global home) /root/composer
ENV PATH=$PATH:/root/composer/vendor/bin COMPOSER_ALLOW_SUPERUSER=1


EXPOSE 80

# Add Scripts

ADD conf/supervisord.conf /etc/supervisord.conf
ADD conf/nginx.conf /etc/nginx/nginx.conf
ADD docker/start.sh /start.sh
RUN chmod 755 /start.sh


WORKDIR "/var/www/html"
CMD ["/start.sh"]