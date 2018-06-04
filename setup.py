from setuptools import setup

setup(
    name='pySupRST',
    version='0.1.2',
    description='little SCADA system',
    author='Loic Lefebvre',
    author_email='loic.celine@free.fr',
    license='MIT',
    url='https://github.com/sourceperl/pySupRST',
    platforms='any',
    py_modules=[
        'pySupRST',
    ],
    scripts=[
        'scripts/srst-db-jobs-srv',
        'scripts/srst-icmp-srv',
        'scripts/srst-mbus-srv',
        'scripts/srst-mbus-exp-srv',
        'scripts/srst_check_tables',
        'scripts/srst_ls_host',
        'scripts/srst_rm_host',
        'scripts/srst_search_host',
        'scripts/srst_sql_builder',
        'scripts/srst_whois_host',
    ],
    install_requires=[
        'schedule',
        'pyModbusTCP',
        'pymysql',
    ],
)
