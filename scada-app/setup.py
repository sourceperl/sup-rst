from setuptools import setup

setup(
    name='pySupRST',
    version='0.1.4',
    description='little SCADA system',
    author='Loïc Lefebvre',
    license='MIT',
    url='https://github.com/sourceperl/pySupRST',
    platforms='any',
    py_modules=[
        'pySupRST',
    ],
    install_requires=[
        'schedule==1.2.2',
        'pyModbusTCP>=0.3.0',
        'pymysql==0.9.3',
    ],
)
