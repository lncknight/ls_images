# Nginx with ModSecurity

Start with `SecRuleEngine DetectionOnly`: log rule matches without blocking requests, then tune before enabling prevention.

## Image

Use Nginx 1.30.6 Alpine, ModSecurity 3.0.17, its Nginx connector 1.0.4 and OWASP CRS 4.30.0. Pin the multi-platform base digest and verify source archive SHA-256 checksums in the Dockerfile. Compile the connector against the base image's exact Nginx version.

Publish `lncknight/nginx:YYYYMMDD` using the HKT build date. Record the resulting manifest digest from the CI job summary; same-day builds replace the date tag. Push a commit whose message contains `nginx` to trigger the existing build workflow. Build/publish does not deploy the image.

## Integrate mounted configurations

Add this include at the top level of a mounted `nginx.conf`, before `events`:

```nginx
include /etc/modsecurity/nginx-main.conf;
```

Add this include inside its `http` block:

```nginx
include /etc/modsecurity/nginx-http.conf;
```

Keep these includes outside the mounted `conf.d` directory. The image adds them to its default configuration, but a bind mount replaces that file. The local consumer `/Users/lawrence/www/ls/ls-nginx.conf/docker-compose.yml` mounts both `nginx.conf` and `conf.d`; add both includes to that consumer before rollout. This image change does not edit the consumer or select its deployment tag.

Preserve existing listeners, upstreams, certificates and mounts. Check `nginx -t` with the actual mounted configuration before recreating the edge container; loading a dynamic module requires restarting the old Nginx process. Inspect `nginx -T` afterward to confirm both includes and the inherited `modsecurity on` setting. A standalone image check does not establish coverage for mounted sites or locations that bypass request access phases, such as immediate `return` directives.

## Tune false positives

Use the shipped paranoia level 1, inbound anomaly threshold 5 and request-only inspection. Keep Nginx's existing 20 MiB request limit; ModSecurity uses the same total and non-file limits. DetectionOnly processes oversized bodies partially rather than rejecting them; inspect body-limit alerts before enabling blocking. Limits in individual Nginx locations still apply.

Review `/var/log/nginx/modsecurity-audit.log` across representative business traffic. Record host, URI, rule ID, parameter and a safe reproducer for each confirmed false positive. The existing Nginx logrotate wildcard covers this file. Restrict log access: header/body sections are omitted, but rule messages can contain matched values.

Mount reviewed exclusion files at `/etc/modsecurity/exclusions-before.conf` and `/etc/modsecurity/exclusions-after.conf` to persist tuning across image replacement. Keep upstream CRS files unchanged. Scope exclusions to the affected host, endpoint, parameter and rule; do not disable SQL injection rules globally or raise thresholds to hide false positives.

For example, place the following runtime exclusion in `exclusions-before.conf` **only after confirming this exact false positive**; replace the sample host, path, argument and rule ID with verified values:

```apache
SecRule REQUEST_HEADERS:Host "@streq example.com" \
    "id:11000,phase:1,pass,nolog,t:none,t:lowercase,chain"
    SecRule REQUEST_URI "@rx ^/profile(?:[?]|$)" \
        "t:none,ctl:ruleRemoveTargetById=942100;ARGS:bio"
```

Re-run the affected legitimate request and malicious requests against other parameters and endpoints after every exclusion. Confirm JSON, form and multipart uploads, login, search and free-text flows in staging. Review error rate, CPU and latency before/after; production acceptance remains separate from the build check.

## Enable blocking and roll back

Mount a reviewed file containing `SecRuleEngine On` at `/etc/modsecurity/engine.conf` after traffic review and staging acceptance. Validate configuration, then reload Nginx. Revert that file to `SecRuleEngine DetectionOnly`, validate and reload to stop WAF blocking while retaining detection.

Keep the previous deployed image digest and configuration for full rollback. Rolling back to an image without ModSecurity also requires reverting the two module/rules includes. Recreate the container when changing image versions.

## Verify

Run the image build in CI or another Docker environment:

```bash
docker buildx build --platform linux/amd64,linux/arm64 nginx \
  --tag lncknight/nginx:$(TZ=Asia/Hong_Kong date +'%Y%m%d')
```

Require the Dockerfile's `verify` stage before producing the final image. It checks `nginx -t`, then proxies to an isolated local backend to exercise benign GET, form, JSON, a body larger than 128 KiB and multipart upload requests. SQL injection in query arguments, JSON and JSON subtypes must pass and leave audit evidence in the shipped DetectionOnly mode, then return 403 in an isolated blocking configuration. Test failures stop publication; the test changes do not enable blocking in the final image.

## Sources

- [ModSecurity Nginx connector](https://github.com/owasp-modsecurity/ModSecurity-nginx)
- [ModSecurity recommended configuration](https://github.com/owasp-modsecurity/ModSecurity/blob/v3.0.17/modsecurity.conf-recommended)
- [CRS false positives and tuning](https://coreruleset.org/docs/2-how-crs-works/2-3-false-positives-and-tuning/)
