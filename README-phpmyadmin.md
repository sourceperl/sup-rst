#  phpMyAdmin setup

## Setup

```bash
# add package (don't configure web server and choose random password)
sudo apt install -y phpmyadmin
```

## Create on admin user on mariaDB to use with phpmyadmin

```bash
# update this
DB_USER="superuser"
DB_PWD="p@ssword"

# execute SQL
cat <<EOF | sudo mysql
CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PWD}';
GRANT ALL PRIVILEGES ON *.* TO '${DB_USER}'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

# clean
unset DB_USER
unset DB_PWD
```
