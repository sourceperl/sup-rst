# Victoriametrics setup

```bash
# create a system account for VM process
sudo useradd --system --shell=/usr/sbin/nologin victoriametrics

# init /opt/vm/ directories
sudo mkdir -p /opt/vm/bin
sudo mkdir -p /opt/vm/data
sudo chown -R victoriametrics:victoriametrics /opt/vm/

# populate bin directory
URL="https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.115.0/victoria-metrics-linux-amd64-v1.115.0.tar.gz"
curl -L ${URL} | sudo tar -xz -C /opt/vm/bin/

# add the vm startup script
cp -v vm/run.sh /opt/vm/

# init supervisord
sudo apt install -y supervisor
sudo cp -v vm/supervisor/vm.conf /etc/supervisor/conf.d/
sudo supervisorctl update
```