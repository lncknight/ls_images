# Docker template from https://gitlab.com/ric_harvey/nginx-php-fpm
# FROM microsoft/mssql-tools as mssql

FROM surnet/alpine-wkhtmltopdf:3.10-0.12.5-full as wkhtmltopdf
# FROM test as wkhtmltopdf
# FROM surnet/alpine-wkhtmltopdf:3.9-0.12.5-full as wkhtmltopdf

FROM richarvey/nginx-php-fpm:1.10.4

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

RUN apk upgrade --update

# basic
RUN buildDeps=" \
    # linux-headers \
    # autoconf \
    # g++ \
    # gcc \
    # libc-dev \
    # make \
    " \
    runtimeDeps=" \
        git \
        nodejs \
        npm \
        rsync \
    " \
    && apk update && apk add $buildDeps $runtimeDeps && apk del $buildDeps

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

# https://stackoverflow.com/questions/49067625/how-can-i-use-chinese-in-alpine-headless-chrome
# https://blog.csdn.net/zimou5581/article/details/101368129
RUN echo @edge http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories


# Install dependencies for wkhtmltopdf
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
  ttf-ubuntu-font-family \
  libpng \
  wqy-zenhei@edge \
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

RUN apk add imagemagick

RUN apk add mysql-client

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
ADD docker/start.sh /start.sh
RUN chmod 755 /start.sh

WORKDIR "/var/www/html"
CMD ["/start.sh"]