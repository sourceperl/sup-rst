# pySupRST
A simple SCADA system for Python

## Setup


```bash
# add packages
sudo apt install -y nmap supervisor python3-setuptools python3-pymysql \
                    python3-requests python3-schedule
# add pySupRST package
sudo python3 setup.py install
# copy tools
sudo cp -v tools/* /usr/local/bin/
```

## Supervisor setup
```bash
# add services
sudo cp -v services/* /usr/local/bin/
# add supervisor config file
sudo cp -v etc/supervisor/conf.d/sup_rst.conf /etc/supervisor/conf.d/
```
