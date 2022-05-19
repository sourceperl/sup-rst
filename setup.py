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
        'schedule',
        'pyModbusTCP',
        'pymysql',
    ],
)
