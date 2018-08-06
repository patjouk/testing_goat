# Where should the config files should go?

## Nginx

staging:

```
/etc/nginx/sites-available/testing-goat-staging.justhiding.org
```
add symlink in `/etc/nginx/sites-enabled/`

## Systemd

staging:

`/etc/systemd/system/gunicorn-testing-goat-staging.justhiding.org.service`