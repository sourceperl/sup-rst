# Grafana setup

## Setup

```bash
# ensure system is up-to-date
sudo apt update && sudo apt upgrade -y
# add required packages
sudo apt install -y apt-transport-https software-properties-common wget
# add the grafana GPG Key
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
# add the grafana repository
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
# install it
sudo apt update && sudo apt install grafana
# apply grafana conf 
sudo cp grafana/grafana.ini /etc/grafana/
sudo chown root:grafana /etc/grafana/grafana.ini
# start grafana
sudo systemctl daemon-reload
sudo systemctl enable grafana-server.service
sudo systemctl start grafana-server.service
# try to login and update the default admin account
echo 'try to login with default admin account (superuser/change_this)'
```

We can also deploy and reload automatically safely if everything is valid with grafana deployment tools:

```bash
./tools/grafana_deploy
```

## Security hardening

> https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-security-hardening/
