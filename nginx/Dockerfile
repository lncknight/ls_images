FROM nginx:1.30.6-alpine@sha256:0e52bd054126cdc040b1276c0af347aeb02a41b9cfe305d6094767ac30e97949 AS base

FROM base AS build

RUN apk add --no-cache build-base autoconf automake libtool pkgconf \
    curl ca-certificates pcre2-dev libxml2-dev yajl-dev linux-headers zlib-dev

WORKDIR /sources

# Pin sources and checksums together; compile the connector for this exact Nginx.
RUN set -eux; \
    curl -fsSL https://github.com/owasp-modsecurity/ModSecurity/releases/download/v3.0.17/modsecurity-v3.0.17.tar.gz -o modsecurity.tar.gz; \
    echo 'f283b33d5c21130fd3a15c84a93a1abe12bd1949edaf44288b12af571b671a50  modsecurity.tar.gz' | sha256sum -c -; \
    mkdir modsecurity; \
    tar -xzf modsecurity.tar.gz --strip-components=1 -C modsecurity; \
    cd modsecurity; \
    ./configure --prefix=/usr/local/modsecurity --disable-static --disable-doxygen-doc \
        --without-curl --without-lmdb --without-lua --without-ssdeep --without-maxmind; \
    make -j"$(nproc)"; \
    make install; \
    strip /usr/local/modsecurity/lib/libmodsecurity.so.*

RUN set -eux; \
    curl -fsSL https://codeload.github.com/owasp-modsecurity/ModSecurity-nginx/tar.gz/refs/tags/v1.0.4 -o connector.tar.gz; \
    echo 'bb596d146ad0650014168dda9dc8d07c50a070010044c95ed0d167a9a78e63a1  connector.tar.gz' | sha256sum -c -; \
    mkdir connector; \
    tar -xzf connector.tar.gz --strip-components=1 -C connector; \
    curl -fsSL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -o nginx.tar.gz; \
    echo '3cf46f5ed7504d460125866b7bea99fb357f31d887e2e63b35503310e9b8b6c8  nginx.tar.gz' | sha256sum -c -; \
    mkdir nginx; \
    tar -xzf nginx.tar.gz --strip-components=1 -C nginx; \
    cd nginx; \
    ./configure --with-compat --add-dynamic-module=../connector; \
    make -j"$(nproc)" modules; \
    strip objs/ngx_http_modsecurity_module.so

RUN set -eux; \
    curl -fsSL https://github.com/coreruleset/coreruleset/releases/download/v4.30.0/coreruleset-4.30.0-minimal.tar.gz -o crs.tar.gz; \
    echo '3d678a41fd5aade34760127fef5dd64fd7a77848913fc0f70dde0cf467c94427  crs.tar.gz' | sha256sum -c -; \
    mkdir /opt/owasp-crs; \
    tar -xzf crs.tar.gz --strip-components=1 -C /opt/owasp-crs; \
    mv /opt/owasp-crs/crs-setup.conf.example /opt/owasp-crs/crs-setup.conf

FROM base AS runtime

ENV ENV=prod

RUN apk add --no-cache bash inotify-tools supervisor tzdata certbot certbot-nginx \
    logrotate libstdc++ pcre2 libxml2 yajl \
    && cp /usr/share/zoneinfo/Asia/Hong_Kong /etc/localtime \
    && mkdir -p /etc/modsecurity /var/cache/modsecurity \
    && chown nginx:nginx /var/cache/modsecurity

COPY --from=build /usr/local/modsecurity/lib/libmodsecurity.so* /usr/local/modsecurity/lib/
COPY --from=build /sources/nginx/objs/ngx_http_modsecurity_module.so /usr/lib/nginx/modules/
COPY --from=build /sources/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
COPY --from=build /sources/modsecurity/unicode.mapping /etc/modsecurity/unicode.mapping
COPY --from=build /opt/owasp-crs /opt/owasp-crs
COPY modsecurity/ /etc/modsecurity/
COPY start.sh /start.sh
COPY logrotate.d/nginx /etc/logrotate.d/nginx

# Bind-mounted nginx.conf files must include these two files too (see README).
RUN sed -i 's|^SecUnicodeMapFile .*|SecUnicodeMapFile /etc/modsecurity/unicode.mapping 20127|' /etc/modsecurity/modsecurity.conf \
    && sed -i '1i include /etc/modsecurity/nginx-main.conf;' /etc/nginx/nginx.conf \
    && sed -i '/^http {/a\    include /etc/modsecurity/nginx-http.conf;' /etc/nginx/nginx.conf

# Gate both target architectures on a real request/response check before push.
FROM runtime AS verify
COPY tests/check_waf.py /tmp/check_waf.py
RUN nginx -t && python3 /tmp/check_waf.py && touch /tmp/waf-verified

FROM runtime
COPY --from=verify /tmp/waf-verified /usr/local/share/waf-verified
