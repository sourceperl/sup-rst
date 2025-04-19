# Nginx setup

## First step

```bash
# install nginx and PHP-FPM (PHP-FastCGI Process Manager)
sudo apt install nginx php-fpm
```

## Initialization of security accounts

```bash
sudo apt-get install apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd username
```

## Configuration files

The files `/etc/nginx/nginx.conf` and `/etc/nginx/sites-available/site.conf` are available on local nginx/ directory.

Apply changes :
```bash
# add an admin whitelist (see snippets/admin-whitelist.conf.model)
sudo vim /etc/nginx/snippets/admin-whitelist.conf
# copy files
sudo cp nginx/conf.d/security.conf /etc/nginx/
sudo cp nginx/sites-available/site.conf /etc/nginx/sites-available/
# disable default conf
sudo rm /etc/nginx/sites-enabled/default
# enable site conf
sudo ln -s /etc/nginx/sites-available/site.conf /etc/nginx/sites-enabled/
# ensure file consistency
sudo nginx -t
# reload nginx conf
sudo systemctl reload nginx
```

We can also deploy and reload automatically safely if everything is valid with nginx deployment tools:

```bash
./tools/nginx_deploy
```

## add nginx log rotation

```bash
# add logrotate
sudo apt install logrotate
# add conf for nginx
sudo tee /etc/logrotate.d/nginx > /dev/null <<EOL
/var/log/nginx/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -f /run/nginx.pid ] && kill -USR1 \`cat /run/nginx.pid\`
    endscript
}
EOL
# test log rotation for nginx
sudo logrotate -f /etc/logrotate.d/nginx
```

## analyzing nginx logs

```bash
# add goaccess
sudo apt install goaccess
# console report
goaccess /var/log/nginx/access.log --log-format=COMBINED
# HTML report
goaccess /var/log/nginx/access.log --log-format=COMBINED > /tmp/goaccess-report.html
```

## Security hardening

some recommendations here: https://protocolguard.com/resources/nginx-security-hardening/

online security test: 
* https://protocolguard.com/ 
* https://www.immuniweb.com/websec/
