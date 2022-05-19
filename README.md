# pySupRST
A simple SCADA system for Python

## Setup


```bash
# add packages
sudo apt install -y nmap supervisor python3-setuptools python3-pymysql \
                    python3-requests python3-schedule
# add pySupRST package
sudo python3 setup.py install
# copy scripts
sudo cp -v scripts/* /usr/local/bin/
```

## Supervisor setup
```bash
sudo cp -v etc/supervisor/conf.d/sup_rst.conf /etc/supervisor/conf.d/
```
