from distutils.core import setup

#with open('README.rst') as f:
#    readme = f.read()

setup(
    name="pySupRST",
    version="0.0.1",
    description="A simple SCADA system for Python",
#    long_description=readme,
    author="Loic Lefebvre",
    author_email="loic.celine@free.fr",
    license = "MIT",
    url="https://github.com/sourceperl/pySupRST",
    packages=["pySupRST"],
    scripts=['scripts/icmpd.py'],
    platforms="any",
    )
