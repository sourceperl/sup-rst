from setuptools import setup

setup(
    name='pySupRST',
    version='0.1.4',
    description='little SCADA system',
    author='Loic Lefebvre',
    author_email='loic.celine@free.fr',
    license='MIT',
    url='https://github.com/sourceperl/pySupRST',
    platforms='any',
    py_modules=[
        'pySupRST',
    ],
    install_requires=[
        'schedule==0.6.0',
        'pyModbusTCP==0.2.0',
        'pymysql==1.1.1',
    ],
)
