# pySupRST
A simple SCADA system for Python

## Add packages
```bash
sudo apt install -y nmap supervisor python3-setuptools python3-pymysql \
                    python3-requests python3-schedule
```

## Add pySupRST
```bash
sudo python setup.py install
```

## Supervisor setup
```bash
sudo cp etc/supervisor/conf.d/sup_rst.conf /etc/supervisor/conf.d/
```
