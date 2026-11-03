## ls-api

### PHP 8.2–8.5 images

GitHub Actions builds `linux/amd64` and `linux/arm64` images when a pushed commit message contains `ls-api`.
Tags use the HKT build date and short PHP code: `lncknight/ls-api:YYYYMMDD-82` (not `php82` or `8.2.35`).

| Code | PHP version |
| --- | --- |
| `82` | 8.2.35 |
| `83` | 8.3.36 |
| `84` | 8.4.27 |
| `85` | 8.5.12 |

All four builds share `ls-api/Dockerfile.php8`; the workflow pins each PHP base image by digest.
Legacy PHP Dockerfiles and published tags remain unchanged. Application compatibility and production rollout require separate validation.

### API PHP 8.3.36 rollout

Build the shared image with the API-required `bcmath`, `mbstring` and `pcntl` extensions in addition to the existing database, XML, image and Redis extensions. Build-time extension assertions fail when a required module is absent; they do not establish application acceptance. Preserve the application and configuration mounts and the `/root/scripts` and `/root/post_boot_scripts` startup hooks.

Install dcron and expose its foreground daemon at `/usr/sbin/cron` for the API Supervisor configuration, while retaining `/usr/bin/crontab` for its post-boot hook.

Use the revision-specific tag `lncknight/ls-api:8.3.36-<full-git-sha>` emitted by this workflow for deployment instead of reusing `20261022-83`, which API-local CI also builds from a different Debian-based Dockerfile. This shared image remains Alpine-based. The workflow also retains the existing HKT-date tags.

Push an authorized commit containing `ls-api` in its message to trigger the existing multi-platform CI build; verify successful publication before updating API image references. Validate the resulting artifact on lsd3 (`ls-dev03.internal.lovestruck.com`) before production, including Composer platform requirements, web/FPM, queues, cron, PDF output and external integrations. The earlier API-local build and Composer-blocked dev pipeline do not validate this shared image. Build/publish and deployment are separate operations; deployment hosts must pull the selected artifact. Do not run Docker locally when working under the file-edit-only restriction.

Build PHP 8.5 locally with `docker build -f ls-api/Dockerfile.php8 -t ls-api:85 ls-api`.
Keep the existing `/var/www/html` application mount, startup hooks and Nginx site configuration mounts.

### change log

- 20220830 - add imagick & support php8
- 20220827 - add chinese fonts (excluding php72)
- 20220827 - === php version matrix ===
- 20220826 - try php 7.2 (support arm64/v8)
- 20220826 - php 7.3 add php ext
- 20220824-php73 - php 7.3 (support arm64/v8)
- 20220824 - php 7.3 support arm64
- 20220817 - php 7.4 support arm64
- 20220802 - php 7.3 from scratch
- 20220726 - upgrade php 7.4 from scratch
- 20220717 - upgrade 1.9.1 (php7.4)
- 20220714 - nginx format cf

## fork from

https://gitlab.com/ric_harvey/nginx-php-fpm/-/blob/1.10.4/Dockerfile
https://gitlab.com/ric_harvey/nginx-php-fpm

## ls-service2
- 20231011 update ip database

### change log

- 20220824 - add build deps
- 20220817 - arm64 supproted
- 20220613 - update ip database
- 20210905 - upadte base image
- 20210729 - add pm2 rotate
- 20191016 - latast stable

## ls-web-v2
- 20231207 - node 18.19-slim
- 20220817 - arm64 supproted (node 12.22)

### change log

## nginx
- TODO - oauth, logrotate
- 20230225 - certbot
  - chown -R nginx:nginx /var/log/nginx
- 20220804 - 1st

